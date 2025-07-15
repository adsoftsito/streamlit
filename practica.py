import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
from sqlalchemy import text

import json

#key_dict = json.loads(st.secrets["textkey"])
#creds = service_account.Credentials.from_service_account_info(key_dict)
#db = firestore.Client(credentials=creds, project="names-project-demo")

db = firestore.Client.from_service_account_json("keys.json")

dbMetas = db.collection("metas")
st.header("Nueva meta")

meta = st.text_input("meta")
fecha = st.text_input("fecha mm/yyyy")
submit = st.button("Crear nueva meta")


# Once the name has submitted, upload it to the database
if meta and fecha  and submit:
 doc_ref = db.collection("metas").document(meta)
 doc_ref.set({
   "meta": meta, 
   "fecha": fecha,
 })
 st.sidebar.write("Meta insertada correctamente")


# ...
def loadByName(meta):
 metas_ref = dbMetas.where(u'meta', u'==', meta)
 currentMeta = None
 for mymeta in metas_ref.stream():
   currentMeta = mymeta 
 return currentMeta


st.sidebar.subheader("Buscar meta")
metaSearch = st.sidebar.text_input("meta")
btnFiltrar = st.sidebar.button("Buscar")


if btnFiltrar:
 doc = loadByName(metaSearch)
 if doc is None:
   st.sidebar.write("Meta no existe")
 else:
   st.sidebar.write(doc.to_dict())


# ...
st.sidebar.markdown("""---""")
btnEliminar = st.sidebar.button("Eliminar")


if btnEliminar:
 deletename = loadByName(metaSearch)
 if deletename is None:
   st.sidebar.write(f"{metaSearch} no existe")
 else:
   dbMetas.document(deletename.id).delete()
   st.sidebar.write(f"{metaSearch} eliminado")
 #...


st.sidebar.markdown("""---""")
newMeta = st.sidebar.text_input("Actualizar meta")
newFecha = st.sidebar.text_input("Actualizar fecha")

btnActualizar = st.sidebar.button("Actualizar")


if btnActualizar:
 updateMeta = loadByName(metaSearch)
 if updateMeta is None:
   st.write(f"{metaSearch} no existe")
 else:
   myupdateMeta = dbMetas.document(updateMeta.id)
   myupdateMeta.update(
     {
       "meta": newMeta,
       "fecha" : newFecha
     }
   )


# ...


metas_ref = list(db.collection(u'metas').stream())
metas_dict = list(map(lambda x: x.to_dict(), metas_ref))
metas_dataframe = pd.DataFrame(metas_dict)
st.dataframe(metas_dataframe)


st.markdown("""---""")

conn = st.connection("postgresql", type="sql")

st.header("Registro Visitas")

usuario = st.text_input("usuario")
comentario = st.text_input("comentario")
submitVisita = st.button("Crear nueva visita")


# Once the name has submitted, upload it to the database
if usuario and comentario  and submitVisita:
#  with conn.session as s:
#    conn.execute(text("INSERT INTO users (name, email, password) VALUES (:name, :email, :password)"), [{"name": "John", "email": "john@example.com", "password": "password"}])
  #cur = conn.cursor()
  #conn.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", (value1, value2))

  #conn.execute("INSERT INTO visitas(usuario, comentario) VALUES (:usuario, :comentario)", params={"usuario": usuario, "comentario": comentario})
  #conn.execute("INSERT INTO visitas(usuario, comentario) VALUES (%s, %s)",  (usuario,  comentario))
  
  #conn.commit()
  #conn._instance.execute("INSERT INTO visitas (usuario, comentario) VALUES (:usuario, :comentario)", params={"usuario": usuario, "comentario": comentario})
  #conn.commit()
  with conn.session as session:
    session.execute(
        text("INSERT INTO visitas(usuario, comentario) VALUES (:usuario, :comentario)"),
        {"usuario": usuario, "comentario": comentario}
    )
    session.commit()

  st.write("Meta insertada correctamente")

if st.button("Query Postgresql table"):
    #st.write("Connection type:", type(conn))

    # Perform query.
    df = conn.query('SELECT * FROM visitas;', ttl="10m")
    # Print results.
    print(df)
    st.dataframe(df)
    #for row in df.itertuples():
    #    st.write(row)
