![image](https://user-images.githubusercontent.com/84594190/129112665-63e31ac4-bbac-4c4a-a55b-4b8141b55ad2.png)

Now a days. Be a company based on data is essencial to keep growing, minimize cost, make good predictions and on the whole, have your processes under control. The exploratory data analysis is a part needed of any project based on data that. Some projects might need a machine learning model, anothers one might need just a visualization. But, in all of this situations the exploratory data analysis is necessary. It's from it that We must be able to provide insights, importants informations that wouldn't be seen before. And It's an important step to another steps ahead (if there is).

# House Rocket

House Rocket is a digital platform whose business model is the purchase and sale of real estate using technology. The dataset used here contains house sale prices for King County, which includes Seattle. It includes homes sold between May 2014 and May 2015. Houses has many attributes that make them more or less attractive to buyers and sellers, location and time of year can also influence prices. It'll be defined some hyphoteses and I am going to figure out if these hyphoteses are True or not and propose a solution. This project includes Exploratory data analysis only, in order to provide insights as well as vizualizations to make and support decisions based on data. This solution was deployed on heroku and I used Streamlit to presents the whole problem, visualization and solution. Links to access streamlit and dataset are here below.

heroku webapp: https://house-rocket-streamlit.herokuapp.com/

kaggle: https://www.kaggle.com/harlfoxem/housesalesprediction

Where the idea to this project came from: https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/

### Variables Description

- **date**: date of sale
- **price**: selling price
- **bedrooms**: number of bedrooms
- **bathrooms**: number of bathrooms
- **sqft_living**: size of living area in ft²
- **sqft_lot**: lot size in feet²
- **floors**: number of floors
- **waterfront**: ‘1’ if the property is on the waterfront, ‘0’ if not.
- **view**: an index from 0 to 4 of how good the view of the property is (imagine 0 for a property with a view of a dirty alley and 4 for a property with a view of a beautiful park)
- **condition**: house condition, with values from 1 to 5
- **grade**: classification by the quality of the material of the house. Buildings with better materials usually cost more
- **sqft_above**: ft² above ground
- **sqft_basement**: ft² below ground
- **yr_built**: year of construction
- **yr_renovated**: year of renewal. ‘0’ if never renewed
- **zipcode**: 5-digit zip code
- **lat, long**: latitude and longitude
- **squft_livng15**: average size of the closest 15 houses, in feet²
- **sqft_lot15**: average plot size of the 15 closest houses, in feet²
