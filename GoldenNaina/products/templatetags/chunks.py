from django import template
register = template.Library() 

@register.filter(name='chunks')
def chunks(list_data, chunk_size):
  """Yield successive n-sized chunks from list_data."""
  chunk =[]
  i=0
  for data in list_data:
    chunk.append(data)
    i += 1
    if i == chunk_size:
      yield chunk
      i = 0
      chunk = []
  yield chunk

@register.filter(name='range')
def range_filter(value):
    """
    Filter - returns a range from 0 to value.
    """
    return range(value)
