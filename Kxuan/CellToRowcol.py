import os
import re
import sys
from warnings import warn

xls_rowmax = 1048576
xls_colmax = 16384
constant_memory = 0
previous_row = 0
images = []


range_parts = re.compile(r'(\$?)([A-Z]{1,3})(\$?)(\d+)')

def xl_cell_to_rowcol(cell_str):
    """
    Convert a cell reference in A1 notation to a zero indexed row and column.

    Args:
       cell_str:  A1 style string.

    Returns:
        row, col: Zero indexed cell row and column indices.

    """
    if not cell_str:
        return 0, 0

    match = range_parts.match(cell_str)
    col_str = match.group(2)
    row_str = match.group(4)

    # Convert base26 column string to number.
    expn = 0
    col = 0
    for char in reversed(col_str):
        col += (ord(char) - ord('A') + 1) * (26 ** expn)
        expn += 1

    # Convert 1-index to zero-index
    row = int(row_str) - 1
    col -= 1

    return row, col

def convert_cell_args(method):
    """
    Decorator function to convert A1 notation in cell method calls
    to the default row/col notation.

    """
    # def cell_wrapper(self, *args, **kwargs):
    def cell_wrapper(*args, **kwargs):

        try:
            # First arg is an int, default to row/col notation.
            if len(args):
                int(args[0])
        except ValueError:
            # First arg isn't an int, convert to A1 notation.
            new_args = list(xl_cell_to_rowcol(args[0]))
            new_args.extend(args[1:])
            args = new_args

        # return method(self, *args, **kwargs)
        return method(*args, **kwargs)

    return cell_wrapper

# def force_unicode(string):
#     """Return string as a native string"""
#     if sys.version_info[0] == 2:
#         if isinstance(string, unicode):
#             return string.encode('utf-8')
#     return string

# def _check_dimensions(self, row, col, ignore_row=False, ignore_col=False):
def _check_dimensions(row, col, ignore_row=False, ignore_col=False):
    # Check that row and col are valid and store the max and min
    # values for use in other methods/elements. The ignore_row /
    # ignore_col flags is used to indicate that we wish to perform
    # the dimension check without storing the value. The ignore
    # flags are use by set_row() and data_validate.

    dim_rowmin = None
    dim_rowmax = None
    dim_colmin = None
    dim_colmax = None

    # Check that the row/col are within the worksheet bounds.
    if row < 0 or col < 0:
        return -1
    # if row >= self.xls_rowmax or col >= self.xls_colmax:
    if row >= xls_rowmax or col >= xls_colmax:
        return -1

    # In constant_memory mode we don't change dimensions for rows
    # that are already written.
    # if not ignore_row and not ignore_col and self.constant_memory:
    if not ignore_row and not ignore_col and constant_memory:
        # if row < self.previous_row:
        if row < previous_row:
            return -2

    if not ignore_row:
        # if self.dim_rowmin is None or row < self.dim_rowmin:
        if dim_rowmin is None or row < dim_rowmin:
            # self.dim_rowmin = row
            dim_rowmin = row
        # if self.dim_rowmax is None or row > self.dim_rowmax:
        if dim_rowmax is None or row > dim_rowmax:
            # self.dim_rowmax = row
            dim_rowmax = row

    if not ignore_col:
        # if self.dim_colmin is None or col < self.dim_colmin:
        if dim_colmin is None or col < dim_colmin:
            # self.dim_colmin = col
            dim_colmin = col
        # if self.dim_colmax is None or col > self.dim_colmax:
        if dim_colmax is None or col > dim_colmax:
            # self.dim_colmax = col
            dim_colmax = col

    return 0


# def insert_image(self, row, col, filename, options=None):
@convert_cell_args
def insert_image(row, col, filename, options=None):
    """
    Insert an image with its top-left corner in a worksheet cell.

    Args:
        row:      The cell row (zero indexed).
        col:      The cell column (zero indexed).
        filename: Path and filename for image in PNG, JPG or BMP format.
        options:  Position, scale, url and data stream of the image.

    Returns:
        0:  Success.
        -1: Row or column is out of worksheet bounds.

    """
    # Check insert (row, col) without storing.
    # if self._check_dimensions(row, col, True, True):
    if _check_dimensions(row, col, True, True):
        warn('Cannot insert image at (%d, %d).' % (row, col))
        return -1

    if options is None:
        options = {}

    x_offset = options.get('x_offset', 0)
    y_offset = options.get('y_offset', 0)
    x_scale = options.get('x_scale', 1)
    y_scale = options.get('y_scale', 1)
    url = options.get('url', None)
    tip = options.get('tip', None)
    anchor = options.get('positioning', None)
    image_data = options.get('image_data', None)

    if not image_data and not os.path.exists(filename):
        # warn("Image file '%s' not found." % force_unicode(filename))
        warn("Image file '%s' not found." % filename)
        return -1

    # self.images.append([row, col, filename, x_offset, y_offset, x_scale, y_scale, url, tip, anchor, image_data])
    images.append([row, col, filename, x_offset, y_offset, x_scale, y_scale, url, tip, anchor, image_data])

def _prepare_image(self, index, image_id, drawing_id, width, height,
                   name, image_type, x_dpi, y_dpi):
    # Set up images/drawings.
    drawing_type = 2
    (row, col, _, x_offset, y_offset,
        x_scale, y_scale, url, tip, anchor, _) = self.images[index]

    width *= x_scale
    height *= y_scale

    # Scale by non 96dpi resolutions.
    width *= 96.0 / x_dpi
    height *= 96.0 / y_dpi

    dimensions = self._position_object_emus(col, row, x_offset, y_offset,
                                            width, height)

    # Convert from pixels to emus.
    width = int(0.5 + (width * 9525))
    height = int(0.5 + (height * 9525))

    # Create a Drawing obj to use with worksheet unless one already exists.
    if not self.drawing:
        drawing = Drawing()
        drawing.embedded = 1
        self.drawing = drawing

        self.external_drawing_links.append(['/drawing',
                                            '../drawings/drawing'
                                            + str(drawing_id)
                                            + '.xml', None])
    else:
        drawing = self.drawing

    drawing_object = [drawing_type]
    drawing_object.extend(dimensions)
    drawing_object.extend([width, height, name, None, url, tip, anchor])

    drawing._add_drawing_object(drawing_object)

    if url:
        rel_type = "/hyperlink"
        target_mode = "External"

        if re.match('(ftp|http)s?://', url):
            target = url

        if re.match('external:', url):
            target = url.replace('external:', '')

        if re.match("internal:", url):
            target = url.replace('internal:', '#')
            target_mode = None

        self.drawing_links.append([rel_type, target, target_mode])

    self.drawing_links.append(['/image',
                               '../media/image'
                               + str(image_id) + '.'
                               + image_type])