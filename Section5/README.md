### Section 5 - Machine Learning
---
  
- In the notebook, H2O automl is used for fast training and evaluation of various classification methods, including xgboost, GBM and ensembled methods.
- To set up H2O for python, refer to the guide from the [official documentation](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/downloading.html#install-in-python)
- The best performing model from automl training is a StackedEnsemble, which has model accurary of over 40% on training datasets (with cross-validations), and 30% on the test set.
- Predicted buying price using the given parameters is "*low*".