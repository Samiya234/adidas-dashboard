import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go


#reading data from excel sheet
df = pd.read_excel('Adidas.xlsx')
st.set_page_config(layout = 'wide')
st.markdown('<style>div.block_container{padding-top:1rem;}</style>' , unsafe_allow_html= True)
image = Image.open('adidas-logo.jpg')

col1 , col2 = st.columns([0.1,0.9])
with col1:
    st.image(image,width=100)


html_title = """
     <style>
     .title-test {
     font - weight : bold;
     padding : 5px;
     border-radius : 6px
     }
     </style>
     <center><h1 class = "title-test"> Adidas Sales Dashboard </h1></center>"""

with col2:
    st.markdown(html_title , unsafe_allow_html=True)


col3 , col4 , col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime('%d/%m/%Y'))
    st.write(f"Last updated by: \n {box_date}")

with col4:
    fig = px.bar(df , x= "Retailer" , y = "TotalSales" , labels={"TotalSales" : "Total Sales {$}"} ,
                 title= " Total Sales by Retailer" , hover_data= ["TotalSales"],
                 template="gridon", height=500)
    st.plotly_chart(fig,use_container_width=True)

_,view1 , dwn1 , view2 , dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer" , "TotalSales"]].groupby(by = "Retailer")["TotalSales"].sum()
    expander.write(data)

with dwn1:
    st.download_button("Data" , data = data.to_csv().encode("utf-8"),
                       file_name = "Retailer_csv" , mime= "text/csv")


df["Month_year"] = df["InvoiceDate"].dt.strftime("%b' %y")
result = df.groupby(by = df["Month_year"])["TotalSales"].sum().reset_index()



with col5:
    fig1 = px.line(result, x = "Month_year" , y = "TotalSales" , 
                   title = "Total Sales over time" , template="gridon")
    
    st.plotly_chart(fig1 ,use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)

with dwn2:
    st.download_button("Data" , data = result.to_csv().encode("utf-8"),
                       file_name = "Montly Sales csv" , mime= "text/csv")


st.divider()

result1 = df.groupby(by = "State")[["TotalSales", "UnitsSold"]].sum().reset_index()


# adding units sold as a line chart on a secondary axis (y - axis) , as in
# total sales will be bar and units sold will be line chart.

fig3 = go.Figure()
fig3.add_trace(go.Bar(x= result1["State"], y = result1['TotalSales']
                      , name = "Total Sales" ))
fig3.add_trace(go.Scatter( x = result1["State"] , y = result1["UnitsSold"] ,
                           mode= "lines" , name = "Units Sold", yaxis = "y2"))
fig3.update_layout(
    title= "Total Sales and Units sold by States",
    xaxis = dict(title = "State"),
    yaxis = dict(title = "Total Sales" , showgrid = False),
    yaxis2 = dict(title = "Units sold" , overlaying = "y" , side = "right"),
    template = "gridon",
    legend = dict(x=1,y=1.2)
)

_,col6 = st.columns([0.1,1])

with col6:
    st.plotly_chart(fig3 , use_container_width=True)
    

_ , view3 , dwn3 = st.columns([0.5 , 0.45 , 0.45])
with view3:
    expander = st.expander("View Data for sales by Units sold")
    expander.write(result1)

with dwn3:
    st.download_button("Data" , data = result1.to_csv().encode("utf-8")
                       , file_name = "Sales by units" , mime="text/csv" )
    
st.divider()

# Treemap chart 

_, col7 = st.columns([0.1,1])

treemap  = df[["Region" , "City" , "TotalSales"]].groupby(by = ["Region" , "City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value>= 0:
        return "{:.2f} Lakh".format(value/100000)
    

treemap ["TotalSales(formatted)"] = treemap["TotalSales"].apply(format_sales)


fig4 = px.treemap(treemap, path= ["Region" , "City"] , values= "TotalSales" ,
                  hover_data= ["TotalSales(formatted)"] , 
                  color= "City" , height= 700 , width= 600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Reigon amd City in treemap")
    st.plotly_chart(fig4 , use_container_width= True)


_ , veiw4 , dwn4 = st.columns([0.5,0.45,0.45])
with veiw4:
    expander = st.expander("Total Sales by Reigon amd City")
    expander.write(treemap)

with dwn4:
    st.download_button("Data" , data = treemap.to_csv().encode("utf-8")
                       , file_name = "Total Sales by Reigon amd City" , mime="text/csv" )
    

_ , view5 , dwn5 = st.columns([0.5,0.45,0.45])
with view5:
    expander = st.expander("View Raw Data")
    expander.write(df)

with dwn5:
    st.download_button("Raw Data" , data = df.to_csv().encode('utf-8') , 
                       file_name = "Raw Data" , mime="text/csv" )
    
st.divider()