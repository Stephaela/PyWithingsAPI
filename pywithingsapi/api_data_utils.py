"""
api_data_utils.py module

Module for utility functions for Withings API data
"""
import pandas as pd


def flatten_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Flatten a specific column in the DataFrame if it contains either dictionaries or lists.

    This function checks if all elements in the specified column are dictionaries or lists.
    If they are dictionaries, it normalizes the column and expands it into multiple columns.
    If they are lists, it explodes the column to create a new row for each element in the list.

    Args:
        df (pandas.DataFrame): The input DataFrame containing the column to be flattened.
        col (str): The name of the column to flatten. The column should contain dictionaries or lists.

    Returns:
        pandas.DataFrame: A new DataFrame with the specified column flattened.

    Raises:
        ValueError: If the column contains data types other than dictionaries or lists.
    """
    if df[col].apply(lambda x: isinstance(x, dict)).all():
        # Normalize dictionaries and join back
        return df.drop(columns=[col]).join(pd.json_normalize(df[col]), rsuffix=f'_{col}')
    elif df[col].apply(lambda x: isinstance(x, list)).all():
        # Explode lists
        return df.explode(col).reset_index(drop=True)
    else:
        raise ValueError(f"Column '{col}' must contain either all dictionaries or all lists.")


def recursive_flatten(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recursively flatten all nested structures (dictionaries or lists) in a DataFrame.

    This function iterates over the columns of the DataFrame and flattens any column containing
    nested structures like dictionaries or lists. It continues to do so recursively until no more
    nested structures are present in the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to recursively flatten.

    Returns:
        pandas.DataFrame: The fully flattened DataFrame.

    Raises:
        ValueError: If an error occurs while flattening a specific column.
    """
    nested_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, (dict, list))).all()]
    if not nested_columns:  # Base case: No nested structures left
        return df
    for col in nested_columns:
        try:
            df = flatten_column(df, col)
        except ValueError as e:
            raise ValueError(f"Error processing column '{col}': {e}")
    return recursive_flatten(df)  # Recursively process remaining nested structures


def dict_to_pandas_df(data_dict: dict) -> pd.DataFrame:
    """
    Convert a dictionary to a Pandas DataFrame and recursively flatten any nested structures.

    This function takes a dictionary as input, converts it to a Pandas DataFrame, and then
    recursively flattens any nested dictionaries or lists within the DataFrame.

    Args:
        data_dict (dict): The input dictionary to be converted into a DataFrame.

    Returns:
        pandas.DataFrame: The flattened DataFrame.

    Raises:
        ValueError: If the dictionary cannot be converted to a DataFrame or if any column
                    contains unsupported data types for flattening.
    """
    try:
        initial_df = pd.DataFrame([data_dict])  # Convert the initial data into a DataFrame
    except ValueError as e:
        raise ValueError(f"Cannot convert initial data to DataFrame: {e}")
    return recursive_flatten(initial_df)  # Call recursive function to flatten the DataFrame
