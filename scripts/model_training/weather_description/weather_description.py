from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from ..utils.utils import save_sklearn_model 

def create_weather_description_model(df, model_filename):
    x = df[['humidity', 'pressure', 'temp', 'wind_speed','feels_like', 'sun_horison_angle', 'precipitation', 'wind_direction' ]]
    y = df['y']
    
    model = DecisionTreeClassifier(random_state=0)
    model.fit(x, y)    
    save_sklearn_model(model, model_filename)


