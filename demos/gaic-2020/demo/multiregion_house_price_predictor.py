from flytekit.sdk.tasks import python_task, inputs, outputs, dynamic_task
from flytekit.sdk.types import Types
from flytekit.sdk.workflow import workflow_class, Input

from demo.house_price_predictor import generate_data, save_to_file, fit, predict


@inputs(locations=Types.List(Types.String), number_of_houses_per_location=Types.Integer, seed=Types.Integer)
@outputs(train=Types.List(Types.CSV), val=Types.List(Types.CSV), test=Types.List(Types.CSV))
@python_task(cache=True, cache_version="0.1", cpu_request="1000Mi", memory_request="1Gi")
def generate_and_split_data_multiloc(wf_params, locations, number_of_houses_per_location, seed, train, val, test):
    train_sets = []
    val_sets = []
    test_sets = []
    for loc in locations:
        _train, _val, _test = generate_data(loc, number_of_houses_per_location, seed)
        train_sets.append(save_to_file("train", _train))
        val_sets.append(save_to_file("val", _val))
        test_sets.append(save_to_file("test", _test))
    train.set(train_sets)
    val.set(val_sets)
    test.set(test_sets)


@inputs(multi_train=Types.List(Types.CSV))
@outputs(multi_model=Types.List(Types.Blob))
@dynamic_task(cache=True, cache_version="0.1", cpu_request="200Mi", memory_request="200Mi")
def parallel_fit(wf_params, multi_train, multi_model):
    models = []
    for train in multi_train:
        t = fit(train=train)
        yield t
        models.append(t.outputs.model)
    multi_model.set(models)


@inputs(multi_test=Types.List(Types.CSV), multi_models=Types.List(Types.Blob))
@outputs(predictions=Types.List(Types.List(Types.Float)), accuracies=Types.List(Types.Float))
@dynamic_task(cache_version='1.0', cache=True, memory_limit="200Mi")
def parallel_predict(wf_params, multi_test, multi_models, predictions, accuracies):
    preds = []
    accs = []
    for test, model in zip(multi_test, multi_models):
        p = predict(test=test, model_ser=model)
        yield p
        preds.append(p.outputs.predictions)
        accs.append(p.outputs.accuracy)
    predictions.set(preds)
    accuracies.set(accuracies)


@workflow_class
class MultiRegionHousePricePredictionModelTrainer(object):
    """
    This pipeline trains an XGBoost model, also generated synthetic data and runs predictions against test dataset
    """
    regions = Input(Types.List(Types.String), default=["SFO", "SEA", "DEN"],
                    help="Regions for where to train the model.")
    seed = Input(Types.Integer, default=7, help="Seed to use for splitting.")
    num_houses_per_region = Input(Types.Integer, default=1000,
                                  help="Number of houses to generate data for in each region")

    # the actual algorithm
    split = generate_and_split_data_multiloc(locations=regions, number_of_houses_per_location=num_houses_per_region,
                                             seed=seed)
    # fit_task = fit(train=split.outputs.train)
    # predicted = predict(model_ser=fit_task.outputs.model, test=split.outputs.test)
    #
    # # Outputs: joblib seralized model and accuracy of the model
    # model = Output(fit_task.outputs.model, sdk_type=Types.Blob)
    # accuracy = Output(predicted.outputs.accuracy, sdk_type=Types.Float)
