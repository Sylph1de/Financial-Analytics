import streamlit as st

from resources.full_view.resources.filtering import get_filters, get_query


def get_full_view(__df):
  columns = st.columns([1, 2])
  try:
    with columns[0]:
      exploring_df = __df.copy(deep=True)
      with st.expander('Ordenamiento', expanded=True):
        sorting = st.radio('Ordenamiento', __df.columns, label_visibility='collapsed', horizontal=True)
        sub_columns = st.columns(3)
        with sub_columns[0]:
          is_asc = st.checkbox('Ascendente', value=True)
        with sub_columns[2]:
          if st.button('Ordenar', use_container_width=True):
            exploring_df.sort_values(by=sorting, ascending=is_asc, inplace=True)
      with st.expander('Filtrado', expanded=True):
        filtering_columns = st.multiselect('Columnas', options=__df.columns)
        sub_columns = st.columns(3)
        with sub_columns[0]:
          exclusive = st.checkbox('Excluyente', value=True)
        filters = get_filters(__df, filtering_columns)
        query = get_query(filters, exclusive)
        with sub_columns[2]:
          if st.button('Filtrar', use_container_width=True):
            if query != '':
              exploring_df = exploring_df.query(query)
            else:
              exploring_df = __df.copy(deep=True)
      exploring_df.Fecha = exploring_df.Fecha.apply(lambda x: x.to_pydatetime().date().strftime('%d-%b-%Y'))
      exploring_df.Gasto = exploring_df.Gasto.astype(str).apply(lambda x: '$' + x)
      exploring_df.Ingreso = exploring_df.Ingreso.astype(str).apply(lambda x: '$' + x)
      exploring_df = exploring_df.style.set_properties(**{'color': 'rgb(255, 115, 115)'}, subset=['Gasto'])
      exploring_df = exploring_df.set_properties(**{'color': 'rgb(115, 255, 115)'}, subset=['Ingreso'])
      exploring_df = exploring_df.set_properties(**{'color': 'cyan'}, subset=['Tipo'])
    with columns[1]:
      st.table(exploring_df)
  except Exception:
    with columns[1]:
      st.info('Aún no tenés registros para mostrar', icon='😔')
