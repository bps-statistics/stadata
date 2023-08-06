# STADATA - Simplified Access to [WebAPI](https://webapi.bps.go.id/developer/) BPS

[![pyversion](https://img.shields.io/pypi/pyversions/stadata-semver)](https://img.shields.io/pypi/pyversions/stadata-semver)
[![pypi](https://img.shields.io/pypi/v/stadata-semver)](https://img.shields.io/pypi/v/stadata-semver)
[![status](https://img.shields.io/pypi/status/stadata-semver)](https://img.shields.io/pypi/status/stadata-semver)
[![downloads](https://img.shields.io/pypi/dm/stadata-semver.svg)](https://img.shields.io/pypi/dm/stadata-semver.svg)
[![sourcerank](https://img.shields.io/librariesio/sourcerank/pypi/stadata-semver.svg)](https://img.shields.io/librariesio/sourcerank/pypi/stadata-semver.svg)
[![contributors](https://img.shields.io/github/contributors/bps-statistics/stadata)](https://img.shields.io/github/contributors/bps-statistics/stadata)
[![license](https://img.shields.io/github/license/bps-statistics/stadata)](https://img.shields.io/github/license/bps-statistics/stadata)

<div align="center">
<!--   <img src="https://github.com/bps-statistics/stadata/assets/1611358/72ac1fab-900f-4a44-b326-0f7b7707668c" width="40%"> -->
  <img src="https://github.com/bps-statistics/stadata/assets/1611358/5a52b335-8e7c-4198-9d4a-7650fe4004da" width="100%">
</div>

## Introduction

STADATA is a Python package that simplifies access to statistical data provided by BPS - Statistics Indonesia, National Statistics Office of Indonesia. BPS offers a [WebAPI](https://webapi.bps.go.id/developer/) - https://webapi.bps.go.id/developer/ that allows users to programmatically access various types of data, including Publications, Press Releases, static tables, and dynamic tables.

With STADATA, Python users can utilize this WebAPI to retrieve data directly from Python scripts, providing users with a convenient and easy-to-use interface to interact with the WebAPI BPS. The package aims to facilitate public access to the data generated by BPS - Statistics Indonesia and eliminate the need for manual data downloads from the [https://www.bps.go.id/](https://www.bps.go.id/).

The key features of STADATA include:

- Access to WebAPI BPS: STADATA enables users to access the BPS official data and retrieve it using Python.
- Easy Installation: The package can be easily installed using pip, making it accessible to Python users.
- Convenient API Methods: STADATA offers simple and straightforward API methods for listing domains, static tables, dynamic tables, and viewing specific tables.
- Language Support: Users can choose between Indonesian ('ind') and English ('eng') languages to display the retrieved data.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
  - [Getting Started](#getting-started)
  - [API Methods](#api-methods)
    - [List Domain](#list-domain)
    - [List Static Table](#list-static-table)
    - [List Dynamic Table](#list-dynamic-table)
    - [List Press Release](#list-press-release)
    - [List Publication](#list-publication)
    - [View Static Table](#view-static-table)
    - [View Dynamic Table](#view-dynamic-table)
    - [View Press Release](#view-press-release)
    - [View Publication](#view-publication)

## Installation

To install STADATA, use the following pip command:

```python
pip install stadata
```

## Requirements

STADATA is designed for Python 3.7 and above. To use the package, the following dependencies are required:

- [requests](https://pypi.org/project/requests/): A library used for making HTTP requests to the WebAPI BPS.
- [html](https://pypi.org/project/html/): A library used for processing HTML content from the API response.
- [pandas](https://pypi.org/project/pandas/): A library used for generate dataframe output for data manipulation and analysis.
- [tqdm](https://pypi.org/project/tqdm/): A library used for adding progress bars to data retrieval operations.

With the necessary requirements in place, you can easily start utilizing STADATA to access the WebAPI BPS and retrieve statistical data from BPS - Statistics Indonesia directly in your Python scripts.

## Usage

To begin using STADATA, you must first install the package and satisfy its requirements, as mentioned in the previous section. Once you have the package installed and the dependencies in place, you can start accessing statistical data from BPS - Statistics Indonesia through the WebAPI BPS.

### Getting Started

To get started with STADATA, you will need an API token from WebAPI BPS. Once you have obtained your token, you can use it to set up the STADATA client in your Python script:

```python
import stadata

# Replace 'token' with your actual API token obtained from WebAPI BPS - https://webapi.bps.go.id/developer/
client = stadata.Client('token')

```

Parameter:

- `token` (str, _required_): Your personal API token provided by the WebAPI BPS Developer portal. This token is necessary to authenticate and access the API. Make sure to replace `token` with your actual API token.

### API Methods

The STADATA package provides the following API methods:

- [List Domain](#list-domain): This method returns a list of BPS's webpage domains from the national level to the district/region level. Domains are used to specify the region from which data is requested.
- [List Static Table](#list-static-table): This method returns a list of all static tables available on the BPS's webpage.
- [List Dynamic Table](#list-dynamic-table): This method returns a list of all dynamic tables available on the BPS's webpage.
- [List Press Release](#list-press-release): This method returns a list of all press release available on the BPS's webpage.
- [List Publication](#list-publication): This method returns a list of all publication available on the BPS's webpage.
- [View Static Table](#view-static-table): This method returns data from a specific static table.
- [View Dynamic Table](#view-dynamic-table): This method returns data from a specific dynamic table.
- [View Press Release](#view-press-release): This method returns data from a specific press release content.
- [View Publication](#view-publicatione): This method returns data from a specific publication.

#### List Domain

This method returns a list of BPS's webpage domains from the national level to the district level. Domains are used to specify the region from which data is requested.

```python
client.list_domain()
```

Returns:

- `domains`: A list of domain IDs for different regions, e.g., provinces, districts, or national.

#### List Static Table

This method returns a list of all static tables available on the BPS's webpage. You can specify whether to get all static tables from all domains or only from specific domains.

```python
# Get all static tables from all domains
client.list_statictable(all=True)

# Get static tables from specific domains
client.list_statictable(all=False, domain=['domain_id-1', 'domain_id-2'])
```

Parameters:

- `all` (bool, _optional_): A boolean indicating whether to get all static tables from all domains (_True_) or only from specific domains (_False_).
- `domain` (list of str, _required_ if `all` is _False_): A list of domain IDs which you want to retrieve static tables from.

Returns:

- `data`: A list of static table information

  ```
  table_id|title|subj_id|subj|updt_date|size|domain
  ```

#### List Dynamic Table

This method returns a list of all dynamic tables available on the BPS's webpage. You can specify whether to get all dynamic tables from all domains or only from specific domains.

```python
# Get all static tables from all domains
client.list_dynamictable(all=True)

# Get static tables from specific domains
client.list_dynamictable(all=False, domain=['domain_id-1', 'domain_id-2'])
```

Parameters:

- `all` (bool, _optional_): A boolean indicating whether to get all static tables from all domains (_True_) or only from specific domains (_False_).
- `domain` (list of str, _required_ if `all` is _False_): A list of domain IDs which you want to retrieve static tables from.

Returns:

- `data`: A list of static table information

  ```
  var_id|title|sub_id|sub_name|subcsa_id|subcsa_name|notes|vertical|unit|graph_id|graph_name|domain
  ```

#### List Publication

This method returns a list of all publication available on the BPS's webpage. You can specify whether to get all publication from all domains or only from specific domains. You can also specify month and year when publication published to get specific publication.

```python
# Get all static tables from all domains
client.list_publication(all=True)

# Get static tables from specific domains
client.list_publication(all=False, domain=['domain_id-1', 'domain_id-2'])

# Get static tables from specific domains, year, and month
client.list_publication(all=False, domain=['domain_id-1', 'domain_id-2'], month="4", year="2022")
```

Parameters:

- `all` (bool, _optional_): A boolean indicating whether to get all publication from all domains (_True_) or only from specific domains (_False_).
- `domain` (list of str, _required_ if `all` is _False_): A list of domain IDs which you want to retrieve publication from.
- `month` (str, _optional_): A month when publication published.
- `year` (str, _required_): A year when publication published.

Returns:

- `data`: A list of publication

  ```
  pub_id|title|issn|sch_date|rl_date|updt_date|size|domain
  ```

#### List Press Release

This method returns a list of all press release available on the BPS's webpage. You can specify whether to get all press release content from all domains or only from specific domains. You can also specify month and year when press release published to get specific press release.

```python
# Get all static tables from all domains
client.list_pressrelease(all=True)

# Get static tables from specific domains
client.list_pressrelease(all=False, domain=['domain_id-1', 'domain_id-2'])

# Get static tables from specific domains, year, and month
client.list_pressrelease(all=False, domain=['domain_id-1', 'domain_id-2'], month="4", year="2022")
```

Parameters:

- `all` (bool, _optional_): A boolean indicating whether to get press release from all domains (_True_) or only from specific domains (_False_).
- `domain` (list of str, _required_ if `all` is _False_): A list of domain IDs which you want to retrieve press release from.
- `month` (str, _optional_): A month when press release published.
- `year` (str, _required_): A year when press release published.

Returns:

- `data`: A list of press release

  ```
  brs_id|subj_id|subj|title|rl_date|updt_date|size|domain
  ```

#### View Static Table

This method returns data from a specific static table. You need to provide the domain ID and the table ID, which you can get from the list of static tables.

```python
# View static table in Indonesian language (default)
client.view_statictable(domain='domain_id', table_id='table_id', lang='ind')
```

Parameters:

- `domain` (str, _required_): The domain ID where the static table is located.
- `table_id` (str, _required_): The ID of the specific static table you want to retrieve data from.
- `lang` (str, _optional_, default: `ind`): The language in which the table data should be displayed (`ind` for Indonesian, `eng` for English).

Returns:

- `data`: The static table data in the specified language.

#### View Dynamic Table

This method returns data from a specific dynamic table. You need to provide the domain ID, variable ID, and the period (year) for the dynamic table.

```python
# View dynamic table with a specific period
client.view_dynamictable(domain='domain_id', var='variable_id', th='year')
```

Parameters:

- `domain` (str, _required_): The domain ID where the dynamic table is located.
- `var` (str, _required_): The ID of the specific variable in the dynamic table you want to retrieve data from.
- `th` (str, _optional_, default: ''): The period (year) of the dynamic table data you want to retrieve.

Returns:

- `data`: The dynamic table data for the specified variable and period.

#### View Publication

This method returns data from a specific publication. You need to provide the domain ID, publication ID for the publication.

```python
# View dynamic table with a specific period
client.view_publication(domain='domain_id', idx='publication_id')
```

Parameters:

- `domain` (str, _required_): The domain ID where the publication is located.
- `idx` (str, _required_): The ID of the specific publication in the list of publication you want to retrieve data from.

Returns:

- `Material`: Object interface for publication and press release content.

Methods:

- `desc()` : Show all detail data of spesific publication
- `download(url)`: Download publication content in PDF

#### View Press Release

This method returns data from a specific press release. You need to provide the domain ID, press release ID for the spesific press release.

```python
# View dynamic table with a specific period
client.view_pressrelease(domain='domain_id', idx='press_release_id')
```

Parameters:

- `domain` (str, _required_): The domain ID where the press release is located.
- `idx` (str, _required_): The ID of the specific press release in the list of press release you want to retrieve data from.

Returns:

- `Material`: Object interface for publication and press release content.

Methods:

- `desc()` : Show all detail data of spesific press release
- `download(url)`: Download press release content in PDF
