---
permalink: /api/graph-data-modeler/
title: GraphDataModeler
toc: true
toc_label: GraphDataModeler
toc_icon: "fa-solid fa-plane"
---

    from neo4j_runway import GraphDataModeler




## Class Methods


### __init__
Takes an LLM instance and Discovery information.
    Either a Discovery object can be provided, or each field
        can be provided individually.

    Attributes
    ----------
    llm : LLM
        The LLM used to generate data models.
    discovery : Union[str, Discovery], optional
        Either a string containing the LLM generated
        discovery or a Discovery object that has been run.
        If a Discovery object is provided then the remaining
        discovery attributes don't need to be provided, by
        default ""
    user_input : Dict[str, UserInput], optional
        Either a dictionary with keys general_description
        and column names with descriptions or a UserInput
        object, by default {}
    general_data_description : str, optional
        A general data description provided by Pandas, by
        default ""
    numeric_data_description : str, optional
        A numeric data description provided by Pandas, by
        default ""
    categorical_data_description : str, optional
        A categorical data description provided by Pandas,
        by default ""
    feature_descriptions : str, optional
        Feature (column) descriptions provided by Discovery,
        by default ""
    allowed_columns : List[str], optional
        The columns that may be used in the data model. The
        argument should only be used in no columns are
        specified in
        the discovery or user_input arguments. By default []


### create_initial_model
Generate the initial model. This must be ran before a
        model can be interated on.
    You may access this model with the `get_model` method
        and providing `version=1`.

    Returns
    -------
    DataModel
        The generated data model.


### get_model
Get the data model version specified.
    By default will return the most recent model.
    Version are 1-indexed.

    Parameters
    ----------
    version : int, optional
        The model version, 1-indexed, by default -1
    as_dict : bool, optional
        whether to return as a Python dictionary. Will
        otherwise return a DataModel object, by default
        False

    Returns
    -------
    Union[DataModel, Dict[str, Any]]
        The data model in desired format.

    Examples
    --------
    >>> gdm.get_model(1) == gdm.model_history[0]
    True


### iterate_model
Iterate on the current model. A data model must exist in
        the `model_history` property to run.

    Parameters
    ----------
    iterations : int, optional
        How many times to perform model generation. Each
        successful iteration will be appended to the
        GraphDataModeler model_history.
        For example if a value of 2 is provided, then two
        successful models will be appended to the
        model_history. Model generation will use the same
        prompt for each generation attempt. By default 1
    user_corrections : Union[str, None], optional
        What changes the user would like the LLM to address
        in the next model, by default None
    use_yaml_data_model : bool, optional
        Whether to pass the data model in yaml format to the
        generation prompt.
        This takes less tokens, but differs from the output
        format of json. By default False

    Returns
    -------
    DataModel
        The most recent generated data model.


### load_model
Append a new data model to the end of the
        `model_history`.
    This will become the new `current_model`.

    Parameters
    ----------
    data_model : DataModel
        The new data model.

    Raises
    ------
    ValueError
        If the data_model is not an instance of DataModel.



## Class Properties


### current_model
Get the most recently created or loaded data model.

    Returns
    -------
    DataModel
        The current data model.


### current_model_viz
Visualize the most recent model with Graphviz.

    Returns
    -------
    Digraph
        The object to visualize.

