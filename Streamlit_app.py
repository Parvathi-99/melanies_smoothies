# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """)
#option = st.selectbox(t
 #   "What is your favorite fruit?",
  #  ("Banana", "Strawberries", "peaches"),
#)
#st.write("Favorite fruit is :", option)

#st.write(st.secrests["snowflake"])
cnx=st.connection("snowflake",type="snowflake")
session = cnx.session()

name_on_order=st.text_input("Name on Smoothie: ")
st.write("name on you smoothie is : ",name_on_order )
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
ingredients_list=st.multiselect("Choose upto 5 ingredients :",my_dataframe,max_selections=5)
ingredients_string=''
if ingredients_list:
    for fruits_choosen in ingredients_list:
      ingredients_string += fruits_choosen+' '
      st.subheader(fruits_choosen+" about nutrition Information :")
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruits_choosen)
      s_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    st.write(ingredients_string)
my_insert_stmt="""insert into smoothies.public.orders(name_on_order,ingredients) values('"""+name_on_order+"""','"""+ingredients_string+"""')"""
st.write(my_insert_stmt)

time_to_insert=st.button("Submit Order")
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f"Your Smoothie is ordered,{name_on_order} !",icon="✅") 


