import streamlit as st

from resources.tools import append_row, notify


def get_add_data():
  form = st.form('add_data_form', clear_on_submit=True)
  container = st.container()
  with form:
    st.subheader(':red[Nuevo registro]')
    form_data = dict()
    columns = st.columns([1, 2])
    with columns[0]:
      date = st.date_input('Fecha').strftime('%d/%m/%Y')
      form_data['Fecha'] = date
    with columns[1]:
      form_data['Concepto'] = st.text_input('Concepto', placeholder='Por favor introducir un concepto')
    columns = st.columns(3)
    with columns[0]:
      options = sorted(['Ocio', 'Transporte', 'Ingreso', 'Comida', 'Servicio', 'Otros', 'Salida', 'Auto', 'Animales', 'Monotributo', 'Alquiler', 'Deuda'])
      form_data['Tipo'] = st.selectbox(':blue[Tipo]', options=options)
    with columns[1]:
      form_data['Gasto'] = float(st.number_input(':red[Gasto]', step=.0))
    with columns[2]:
      form_data['Ingreso'] = float(st.number_input(':green[Ingreso]', step=.0))
      if st.form_submit_button('Agregar registro', type='primary', use_container_width=True):
        form_data = list(form_data.values())
        if not any([value == '' for value in form_data]):
          append_row(container, form_data)
        else:
          notify(container, 'info', body='Debe llenar todos los campos antes de poder crear el registro.', icon='💡')
