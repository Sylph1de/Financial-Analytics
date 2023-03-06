import streamlit as st


def get_filters(__df, columns):
  filters = dict()
  for col in columns:
    sample = __df[col][0]
    if col == 'Fecha':
      min_value = __df[col].min()
      max_value = __df[col].max()
      filters[col] = st.date_input(col, value=(min_value, max_value), min_value=min_value, max_value=max_value)
    elif isinstance(sample, str):
      st.subheader(col)
      uniques = __df[col].unique()
      filters[col] = st.multiselect(col, options=uniques, default=uniques)
    elif isinstance(sample, int):
      min_value = int(__df[col].min())
      max_value = int(__df[col].max())
      filters[col] = st.slider(col, min_value=min_value, max_value=max_value, value=(min_value, max_value))
    elif isinstance(sample, float):
      min_value = float(__df[col].min())
      max_value = float(__df[col].max())
      filters[col] = st.slider(col, min_value=min_value, max_value=max_value, value=(min_value, max_value))
  return filters


def get_query(filters: dict, exclusive: bool):
  mode = ' & ' if exclusive else ' | '
  query_data = []
  for key, value in filters.items():
    sample = value[0]
    if isinstance(sample, str):
      filter_str = f'{key}.isin({value})'
    elif isinstance(sample, (int, float)):
      filter_str = f'({key} >= {value[0]} & {key} <= {value[1]})'
    else:
      filter_str = f'({key} >= "{value[0]}" & {key} <= "{value[1]}")'
    query_data.append(filter_str)
  query = mode.join(query_data)
  return query
