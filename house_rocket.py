import pandas         as pd
import numpy          as np
import streamlit      as st
import plotly.express as px

from datetime import datetime

st.set_page_config( layout='wide' )

@st.cache( allow_output_mutation=True ) 
def get_data( path ):
    data = pd.read_csv( path )

    return data

def set_feature( data ):
    ##############################################################
    ########################## FEATURE ENGINEERING ###############
    ##############################################################
    data['id']       = data['id'].astype('str')
    data['zipcode']  = data['zipcode'].astype('str')
    data['price_m2'] = data['price']/data['sqft_lot']
    data['date']     = pd.to_datetime( data['date'] )
    data['season']   = 'test'

    data.loc[( data['date'].dt.month >= 6 ) & ( data['date'].dt.month <= 8), 'season'] = 'Summer'
    data.loc[( data['date'].dt.month >= 9 ) & ( data['date'].dt.month <= 11), 'season'] = 'Fall'
    data.loc[( data['date'].dt.month == 12 ), 'season'] = 'Winter'
    data.loc[( data['date'].dt.month == 1 ),  'season'] = 'Winter'
    data.loc[( data['date'].dt.month == 2 ),  'season'] = 'Winter'
    data.loc[( data['date'].dt.month >= 3 ) & ( data['date'].dt.month <= 5), 'season'] = 'Spring'

    data['date'] = pd.to_datetime( data['date'] ).dt.strftime('%Y-%m-%d')
    
    return data

def overviewdata( data ):
    st.markdown('''# 1.0 Business Problem

House Rocket is a digital platform whose business model is the purchase and sale of real estate using technology. 
The dataset used here contains house sale prices for King County, which includes Seattle. 
It includes homes sold between May 2014 and May 2015. 
Houses has many attributes that make them more or less attractive to buyers and sellers, 
location and time of year can also influence prices. 
It'll be defined here below some hyphoteses and I am going to figure out if these hyphoteses are True or not.
        
#### Main goal:
- Maximize company revenue by finding good business opportunities.
    
    
#### Questions:
- Which houses should the CEO of House Rocket buy and at what purchase price?
- Once the house is owned by the company, what is the best time to sell them and what would be the sale price?
- Should House Rocket do a renovation to raise the sale price? What would be the suggestions for changes? What is the price increase given for each refurbishment option?


#### Solution Approach:
- Offer a table which contains the purchased value and price that should be sold. 
Knowing that the price might be affected by location ( which is the feature "Zipcode" ) and Time of year. 
The idea is cluster by these main features through of explolatory data analysis and present that by streamlit 


#### Strategy:
- Buy good houses in great locations at low prices and then resell them later at higher prices.
    The suggestion is going to be: 
    - The houses which are valiated lower to average price per region, it'll be increased 30% in price and it'll be sold. 
    - Show on the same table the best season to buy and sell, based on the  average price per regions during the seasons

#### Hypotheses:
- 0.1 The average house prices differ by 10% between winter and summer
- 0.2 The best season to sell is SUMMER
- 0.3 The house's price is increased when its bedroom's size is increased
- 0.4 The price of the house decreases with the increase in the number of bathrooms
- 0.5 Houses with water view are 15% on average more expensive  
''')

    ##############################################################
    ########################## DATA OVERVIEW #####################
    ##############################################################

    st.sidebar.title( 'General Data Options' )

    f_attributes = st.sidebar.multiselect( 'Enter columns', data.columns )
    f_zipcode    = st.sidebar.multiselect( 'Enter zipcode', data['zipcode'].unique() )

    if ( f_attributes != [] ) & ( f_zipcode != []):
        data = data.loc[ data['zipcode'].isin( f_zipcode ), f_attributes ]

    elif ( f_attributes != [] ) & ( f_zipcode == []):
        data = data.loc[:, f_attributes ]

    elif ( f_attributes == [] ) & ( f_zipcode != []):
        data = data.loc[ data['zipcode'].isin( f_zipcode ),: ]

    else:
        data = data.copy()

    st.title(  '2.0 Data Overview' )
    st.markdown( '''### Added two new features:
- **Price/m2:** Price per square meter (it'll be important to Average price analysis done here below)
-  **Season:**   Seasons of the year ( Winter, Summer, Spring, Fall ) (it'll be important to analyze the price per season)
    ''')
    st.header( 'Data Dimension: Rows: {} Columns: {}' .format( data.shape[0],data.shape[1] ) )
    st.dataframe( data )
    st.header( 'Columns and Missing Values' )
    st.dataframe( data.isnull().sum() )

    ##############################################################
    ########################## METRICS  ##########################
    ##############################################################
    if ( all( [ x in f_attributes for x in ['id','zipcode','price','price_m2','sqft_living'] ] ) == True ) | ( f_attributes == [] ):
        
        c1, c2 = st.columns( (1,1) )

        df_01 = data[['id','zipcode']].groupby( 'zipcode' ).count().reset_index()
        df_02 = data[['price','zipcode']].groupby( 'zipcode' ).mean().reset_index()
        df_03 = data[['sqft_living','zipcode']].groupby( 'zipcode' ).mean().reset_index()
        df_04 = data[['price_m2','zipcode']].groupby( 'zipcode' ).mean().reset_index()

        df_05 = pd.merge( df_01,df_02, on='zipcode', how='inner' )
        df_06 = pd.merge( df_05,df_03, on='zipcode', how='inner' )
        df    = pd.merge( df_06,df_04, on='zipcode', how='inner' )
        df.columns = ['ZIPCODE','TOTAL HOUSES','PRICE','SQRT LIVING','PRICE/m2']
        
        c1.header ( 'Average Values' )
        c2.header( 'Descriptive Analysis' )

        c1.write( '''Here it's showed, The average price per regions(zipcode). We're able to see
        what regions are more expensive than others **(you're able to sort the DataFrame pressing over the name the feature you want to sort)**,
        and what's the maximum and minimum average price per regions
        and find out what regions are cheaper or more expensive. Together with this information you'll be able
        to filter using this interested regions to filter the dataset and make your analysis''' )

        c2.write( '''Here it's showed some descriptive statistics that might be important to make or base decisions''' )
        df_aux = data.describe().T[['mean','50%','min','max','std']]
        df_aux.columns = ['Mean','Median','Min','Max','Std']
        
        c1.dataframe( df, height=400)
        c2.dataframe( df_aux, height=400 )
        
    else: 
        st.write( 'If you want to be able to see the **STATISTICS ANALYSIS** select at least that columns: \n\n **{}**'.format( ['id','zipcode','price','price_m2','sqft_living'] ) ) 

    ##############################################################
    ########################## COMERCIAL ATTRIBUTES ##############
    ##############################################################
    if ( all( [ x in f_attributes for x in ['yr_built','yr_renovated','price','date','season'] ] ) == True ) | ( f_attributes == [] ):
    
        st.title( '3.0 Comercial Attributes' )
        st.markdown('''The Average price of Renovated Properties are in general higher.
        It is worth doing a renovation.
        ''')

        df     = data[['price','yr_renovated']].groupby( 'yr_renovated' ).mean().reset_index()
        df.loc[df['yr_renovated']!=0, 'Renovated'] = 'Yes'
        df.loc[df['yr_renovated']==0, 'Renovated'] = 'No'
        df_aux = df[['Renovated','price']].groupby( 'Renovated' ).mean().reset_index()
        st.dataframe(df_aux)

        c3, c4, = st.columns( (1,1) )

        c3.header( 'Average Price per Year Built' )
        c4.header( 'Average Price per Year Renovated')

        ########
        ## C3 ##
        ########
        min_year_built = int( data['yr_built'].min() )
        max_year_built = int( data['yr_built'].max() )

        c3.subheader( 'Select Max Year Built' )
        f_year_built   = c3.slider( 'Year Built', min_year_built, max_year_built, max_year_built )


        df  = data.loc[data['yr_built']<f_year_built]
        df  = df[['yr_built','price']].groupby( 'yr_built' ).mean().reset_index()
        df['mean'] = df['price'].mean() 
        fig = px.line( df, x='yr_built', y=['price','mean'] ,color_discrete_sequence=['#5F9EA0','#2F4F4F'])

        c3.plotly_chart( fig, use_container_width=True )

        ########
        ## C4 ##
        ########
        min_year_renovated = int( data['yr_renovated'].min() )
        max_year_renovated = int( data['yr_renovated'].max() )

        c4.subheader( 'Select Max Year Built' )
        f_year_renovated   = c4.slider( 'Year Renovated', min_year_renovated, max_year_renovated, max_year_renovated )


        df  = data.loc[data['yr_renovated']<f_year_renovated]
        df  = df[['yr_renovated','price']].groupby( 'yr_renovated' ).mean().reset_index()
        df = df[df['yr_renovated'] != 0]
        df['mean'] = df['price'].mean()
        fig = px.line( df, x='yr_renovated', y=['price','mean'] ,color_discrete_sequence=['#5F9EA0','#2F4F4F'])

        c4.plotly_chart( fig, use_container_width=True )

        c5, c6 = st.columns( (1,1))

        c5.header( 'Average Price per Date' )
        c6.header( 'Price Distribuition' )

        ########
        ## C5 ##
        ########
        c5.write('''As seen here below, there's a point on october 11th in 2014 that are out of line of with others. In my
        researches, I didn't find anything that explain this value. And then, this point likely might be an outlier''')
        c5.subheader( 'Select Max Date' )
        
        min_date = datetime.strptime( data['date'].min(), '%Y-%m-%d' )
        max_date = datetime.strptime( data['date'].max(), '%Y-%m-%d' )
        f_date   = c5.slider( 'Date', min_date, max_date, max_date )

        data['date'] = pd.to_datetime( data['date'] )
        df           = data.loc[data['date']<f_date]
        df           = df[['date','price']].groupby( 'date' ).mean().reset_index()
        fig          = px.line( df, x='date', y='price',color_discrete_sequence=['#5F9EA0'])
        
        c5.plotly_chart( fig, use_container_width=True )

        ########
        ## C6 ##
        ########    
        c6.write( '''The largest number of houses is concentraded in a price between 75 k and 1 M
        
        
        ''')
        c6.subheader( 'Select Max Price' )

        min_price = int( data['price'].min() ) 
        max_price = int( data['price'].max() )
        f_price   = c6.slider( 'Price', min_price, max_price, max_price )

            
        df  = data[data['price']<=f_price]
        fig = px.histogram( df, x='price', nbins=20, color_discrete_sequence=['#5F9EA0'] )
        c6.plotly_chart( fig, use_container_width=True )

        ##############################################################
        ################# PRICE DISTRIBUITION PER SEASON #############
        ##############################################################
        st.title( '4.0 Price Destribuition per Season' )
        st.subheader( 'Mean Price Destribuition per Season' )
        st.markdown('''### **Hyphotese 0.1** 
The average house prices differ under 10% between winter and summer
( **TRUE** )

the average price of winter compared to summer is under 10% 
''')
        df     = data[['price','season']].groupby('season').mean().reset_index()
        differ = ( abs( df['price'][2]-df['price'][3] )/( df['price'][2]))*100
        st.dataframe(df)

        st.write( 'Diference: **{}%**'.format(differ) )

        st.markdown('''### **Hyphotese 0.2** 
The best season to sell is SUMMER
( **FALSE** )

The average price from SUMMER is higher than WINTER ( the winter for instance is the cheaper average price of all ) 
( CONSIDERING ALL REGIONS, diferent regions has diferent average price per season. 
And it'll be considered on analysis on the table recomendation presented here )
''')

        fig = px.bar( df, x='season', y='price', color='season', color_discrete_sequence=['#5F9EA0','#5F9EA0','#5F9EA0','#2F4F4F'] )
        st.plotly_chart( fig, use_container_width=True )

    else:
        st.write( 'If you want to be able to see the **PRICE DISTRIBITION** select at least these columns:\n\n **{}**'.format( ['yr_built','yr_renovated','price','date','season'] ) )


    ##############################################################
    ########################## HOUSE ATTRIBUTES  #################
    ##############################################################
    if ( all( [ x in f_attributes for x in ['bedrooms','price','bathrooms','waterfront'] ] ) == True) | ( f_attributes == [] ):

        st.title( '5.0 House Attibutes' )

        ############
        ## FILTER ##
        ############
        f_bedrooms  = st.selectbox( 'Max Numbers of bedrooms', sorted( set( data['bedrooms'].unique() ) ) )
        f_bathrooms = st.selectbox( 'Max Numbers of bathdrooms', sorted( set( data['bathrooms'].unique() ) ) )

        c1, c2 = st.columns( (1,1) )

        #### BEDROOMS
        c1.header( 'Price per Bedrooms' )
        c1.write( '''It's visible that there's a house that contains 33 bedrooms and a low price ( compared to the other ones ). 
        In my researches I didn't find anything that explain that.
        And then it likely might be an outlier ''')
        c1.markdown('''### **Hyphotese 0.3**
The house's price is increased when its bedroom's size is increased
( **FALSE** )

The price goes up to a certain point and after that, it goes down
''')

        df  = data[data['bedrooms']<=f_bedrooms]
        fig = px.scatter( df, x='bedrooms', y='price', color='price' ,color_continuous_scale=px.colors.sequential.Darkmint)

        c1.plotly_chart( fig, use_container_width=True )

        ##### BATHROOMS
        c2.header( 'Houses per bathrooms' )
        c2.markdown(''' ### **Hyphotese 0.4**
The price of the house decreases with the increase in the number of bathrooms 
( **FALSE** )

There is a tendence of growing. The price goes up to increase of bathrooms
''')

        df  = data[data['bathrooms']<=f_bathrooms]
        fig = px.scatter( df, x='bathrooms', y='price', color='price' ,color_continuous_scale=px.colors.sequential.Darkmint )

        c2.plotly_chart( fig, use_container_width=True )

        #### WATER VIEW
        st.header( 'Water View' )
        st.markdown(''' #### **Hyphotese 0.5**
    Houses with water view are over 15% on average more expensive
    ( **TRUE** )
    ''')

        dfaux  = data[['waterfront','price']].groupby( 'waterfront' ).mean().reset_index()
        if dfaux.shape == (2,2):
            differ = ( ( dfaux['price'][1] - dfaux['price'][0] ) / dfaux['price'][0] )*100
            
            st.write(dfaux)
            dfaux['waterfront'] = dfaux['waterfront'].apply( lambda x: '0 ( No Water View )' if x==0 else '1 ( Water View )')
            st.write( 'Houses with Water View are on average **{}**% more expensive than houses with no Water View'.format(differ))
            
            fig = px.bar( dfaux, x='waterfront', y='price', color_discrete_sequence=['#5F9EA0','#2F4F4F'], color='waterfront')

            st.plotly_chart( fig, use_container_width=True )

    else:
        st.write( 'If you want to be able to see the **HOUSE ATTRIBUTES** select at least these columns:\n\n **{}**'.format( ['bedrooms','price','bathrooms','waterfront'] ) )
    
    #################################################
    ################## GRAPH ########################
    #################################################
    if ( all( [ x in f_attributes for x in ['lat','long','price','id','waterfront'] ] ) == True) | ( f_attributes == [] ):

        f_water_view = st.checkbox( 'Waterview', sorted( set( data['waterfront'].unique() ) ) )
        df = data[data['waterfront']==f_water_view]

        if f_water_view == 0:
            st.title('Amount of Houses with no Water View: {}'.format( df['waterfront'].count() ) )
        else:
            st.title('Amount of Houses with Water View: {}'.format( df['waterfront'].count() ) )

        figg = px.scatter_mapbox(df,
                                lat = 'lat',
                                lon = 'long',
                                hover_name= 'id',
                                size = 'price',
                                color = 'zipcode',
                                color_discrete_sequence = px.colors.sequential.Emrld,
                                size_max = 15,
                                zoom=10)

        figg.update_layout(mapbox_style = 'open-street-map')
        figg.update_layout(height = 600, margin={'r':0,'t':0,'l':0,'b':0})
        st.plotly_chart( figg, use_container_width=True )

    else:
        st.write( 'If you want to be able to see a **MAP** of **HOUSE DISTRIBUITION** select at least these columns:\n\n **{}**'.format( ['lat','long','price','id','waterfront'] ) )

    
    
    if ( all( [ x in f_attributes for x in ['zipcode','price','id','season'] ] ) == True) | ( f_attributes == [] ):

        st.markdown('''# Purchase Recomendation Table
Knowing that the price might be affected by location ( which is the feature "Zipcode" ) and Time of year.
This table presents a recomendation to which houses should the House Rocket's CEO buy, together with the
information about:

- What houses They have to buy and the value to sell
    - The idea was: Based on the average price of the houses, if the house's price was lower than average price per
    zipcode ( Regions ), that house might be bought and sold by its onw price plus 30% increased.
    
- Period to buy and sell (Seasons).
    - As known the time of year might change the value of the houses. The idea was suggest a Season of the year
    to buy and sell that house. Based on the minimum and maximum price per season for each zipcode. What that's mean though?
    on Average, the best time ( clustering all Regions as one ) to buy a house is on Winter, and Selling on Summer.
    Each region has its own variation along the season of the year, and then for each region was select the best season to buy ( minimum average price )
    and the best season to sell ( maximum average price )
''')
        ######################
        ###### Sale Value ####
        ######################
        df_01 = data[['zipcode','price']].groupby( 'zipcode' ).mean().reset_index()
        df_01.rename( columns={'price': 'Average_Price'}, inplace=True )

        df_02 = data[['id','zipcode','price']]

        df_03 = pd.merge( df_02,df_01, on='zipcode' )
        df_03['diference'] = df_03['Average_Price'] - df_03['price']
        df_03['buy']    = df_03['diference'].apply( lambda x: 'Yes' if x>0 else 'No' )
        df_03.loc[df_03['buy']=='Yes', 'Sale_Value'] = df_03['price']+( df_03['price']*0.3 )


        ######################
        ### Season To Buy ####
        ######################
        df_04 = data[['price','season','zipcode']].groupby( ['zipcode','season'] ).mean().reset_index()
        df_05 = df_04[['zipcode','price']].groupby( 'zipcode' ).min().reset_index()
        df_05.rename( columns={'price':'Min_price'}, inplace=True )

        df_06 = pd.merge( df_04, df_05, on='zipcode' )
        df_07 = df_06[df_06['price']==df_06['Min_price']][['zipcode','season']]
        df_07.rename( columns={'season': 'Season to Buy'}, inplace=True )

        df_08 = pd.merge( df_03, df_07, on='zipcode' )

        ######################
        ### Season To Sell ###
        ######################
        df_09 = data[['price','season','zipcode']].groupby( ['zipcode','season'] ).mean().reset_index()
        df_10 = df_04[['zipcode','price']].groupby( 'zipcode' ).max().reset_index()
        df_10.rename( columns={'price':'Max_price'}, inplace=True )

        df_11 = pd.merge( df_09, df_10, on='zipcode' )
        df_12 = df_11[df_11['price']==df_11['Max_price']][['zipcode','season']]
        df_12.rename( columns={'season': 'Season to Sell'}, inplace=True )

        df_13 = pd.merge( df_08, df_12, on='zipcode' )
        df_13.loc[df_13['Sale_Value'].isnull(), ['Season to Buy','Season to Sell']] = np.NaN

        st.dataframe(df_13)
    else:
        st.write( 'If you want to be able to see the final **PURCHASE RECOMENDATION TABLE** select at least these columns:\n\n **{}**'.format( ['zipcode','price','id','season'] ) )
   
    ####################
    #### TOP INSIGHTS ##
    ####################
    st.markdown('''# Top 3 Insights
- **1.0** On General the best season to buy and sell are **"FALL"** and **"SPRING"** in a row
''')

    df_aux_01 = df_13['Season to Buy'].value_counts()
    df_aux_02 = df_13['Season to Sell'].value_counts()

    st.dataframe( df_aux_01 )
    st.dataframe( df_aux_02 )

    st.markdown('''
    - **2.0** About **60%** of the houses contained on the dataset was classified as **"YES"** to be bought and after sold to a higher price.
    ''')

    df_aux_03 = df_13['buy'].value_counts( normalize=True )

    st.dataframe( df_aux_03 )

    st.markdown('''
    - **3.0** As seen on step 5.0 ( House Attributes ). The price goes up to a certain point and after that, 
        it goes down. It is expected that, how much you increase the amount of bedrooms,
        more expensive this property is going to be. In this case, doesn't happen that though. I don't know exactly why, but
        I was just wondering: "it likely might be: What if all properties in the dataset aren't houses only?" what if there was
        a diferent type of property in there, where people go just to sleep. Or even could be the situation: at certain point,
        add new bedrooms inside the house, on the first moment might goes up the price. Otherwhise, when there a lot of bedrooms
        in this house, add a new one likely might cost not too much more.
    ''')

if __name__ == '__main__':
    #ETL
    
    # DATA EXTRATION
    url = 'kc-house-data.csv'
    data = get_data( url )

    # TRASNFORMATION
    data = set_feature( data )

    #overview
    overviewdata( data )