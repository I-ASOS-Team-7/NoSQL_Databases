# SOURCE: https://towardsdatascience.com/create-a-graph-database-in-neo4j-using-python-4172d40f89c4

import json
from typing import List

import pandas as pd


def load_archive_data_to_dataframe(file_path: str, lines: int) -> pd.DataFrame:
	# TODO - Docstring

	metadata  = []
	with open(file_path, 'r') as archive_file:		
		for index, line in enumerate(archive_file):
			metadata.append(json.loads(line))
			if index == lines - 1: break
				
	return pd.DataFrame(metadata)


def get_author_list(line: str) -> List[str]:
    # Cleans author dataframe column, creating a list of authors in the row.
    # TODO - Docstring
    return [e[1] + ' ' + e[0] for e in line]


def get_category_list(line: str) -> List[str]:
    # Cleans category dataframe column, creating a list of categories in the row.
    # TODO - Docstring
    return list(line.split(" "))


def load_and_clean_archive_data(file_path: str, lines: int) -> pd.DataFrame:
    df = load_archive_data_to_dataframe(file_path=file_path, lines=lines)

    df['cleaned_authors_list'] = df['authors_parsed'].map(get_author_list)
    df['category_list'] = df['categories'].map(get_category_list)

    return df.drop(
        [
            'submitter', 
            'authors', 
            'comments', 
            'journal-ref', 
            'doi', 
            'report-no', 
            'license', 
            'versions', 
            'update_date', 
            'abstract', 
            'authors_parsed', 
            'categories'
        ],
        axis=1
    )
