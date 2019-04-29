# modified from https://github.com/amueller/scipy-2018-sklearn/blob/master/notebooks/15.Pipelining_Estimators.ipynb

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from dask_ml.model_selection import GridSearchCV
from dask.distributed import Client
from sklearn.pipeline import make_pipeline
from dask_ml.preprocessing import StandardScaler
from dask_ml.linear_model import LogisticRegression


if __name__ == "__main__":
	client = Client()
	data = Path('./data')
	df = pd.read_csv(data/"01_heights_weights_genders.csv")
	y = 1*(df.Gender == "Male").values
	X = df[['Height', 'Weight']].values
	X_train, X_test, y_train, y_test = train_test_split(X, y)
	pipeline = make_pipeline(StandardScaler(), 
                         LogisticRegression())
	grid = GridSearchCV(pipeline,
                    param_grid={'logisticregression__C': [.1, 1, 10, 100]}, cv=5)
	grid.fit(X_train, y_train)
	print("Score",grid.score(X_test, y_test))
