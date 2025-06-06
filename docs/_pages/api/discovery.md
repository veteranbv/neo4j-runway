---
permalink: /api/discovery/
title: Discovery
toc: true
toc_label: Discovery
toc_icon: "fa-solid fa-plane"
---

    from neo4j_runway import Discovery




## Class Methods


### __init__
The Discovery module that handles summarization and
        discovery generation via an LLM.

    Attributes
    ----------
    llm : LLM, optional
        The LLM instance used to generate data discovery.
        Only required if pandas_only = False.
    user_input : Union[Dict[str, str], UserInput]
        User provided descriptions of the data.
        If a dictionary, then should contain the keys
        "general_description" and all desired columns., by
        default = {}
    data : pd.DataFrame
        The data in Pandas DataFrame format.
    pandas_only : bool
        Whether to only generate discovery using Pandas.
        Will not call the LLM service.


### run
Run the discovery process on the provided DataFrame.
    Access generated discovery with the .view_discovery()
        method of the Discovery class.

    Parameters
    -------
    show_result : bool
        Whether to print the generated discovery upon
        retrieval.
    notebook : bool
        Whether code is executed in a notebook. Affects the
        result print formatting.

    Returns
    ----------
    None


### to_markdown
Write the generated discovery to a Markdown file.

    Parameters
    ----------
    file_dir : str, optional
        The file directory to write to, by default "./"
    file_name : str, optional
        The name of the file, by default "discovery"


### to_txt
Write the generated discovery to a .txt file.

    Parameters
    ----------
    file_dir : str, optional
        The file directory to write to, by default "./"
    file_name : str, optional
        The name of the file, by default "discovery"


### view_discovery
Print the discovery information.

    Parameters
    ----------
    notebook : bool, optional
        Whether executing in a notebook, by default True

    Returns
    ----------
    None

