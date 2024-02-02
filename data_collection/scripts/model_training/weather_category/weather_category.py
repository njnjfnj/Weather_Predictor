from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from ..utils.utils import save_model 

def create_weather_category_model(df, model_filename):
    x = df[['temp', 'feels_like', 'pressure', 'humidity','temp_min','temp_max','wind_speed']]
    y = df['y']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    
    model = DecisionTreeClassifier(random_state=0)
    model.fit(x_train, y_train)    
    save_model(model, model_filename)


