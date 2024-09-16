# PyWithingsAPI

Library in Python for the Withings API

---

## The Withings API

More information about the Withings API can be found in the 
[Withings Developer Portal](https://developer.withings.com/) 
and the [Withings API Reference](https://developer.withings.com/api-reference/)

At first, you create a Withings developer account on the 
[Withings Developer Dashboard](https://developer.withings.com/dashboard/) 
and log in. Then, choose the environment on which your application 
will be running. Only the public cloud is open to everyone. After 
that, choose what kind of application you plan on making. Only the 
public API integration if open to everyone. 

Now enter your application name, description and redirect URL. I chose 
http://localhost:1400/ as my redirect URL, but please note that 
there are some limitations for such a redirect URL (according to 
Withings: "HTTP URLs, localhost and ports other than 80 or 443 are 
not supported for applications running in production. You may use 
them during your integration phase but your application will be 
restricted to 10 users.")

Then, Withings will show you your client ID and client secret. 
Store them safely.

## Getting a token

To access user data, you need a valid access token. When you
want to get your first access token, follow these steps:

### Create new instances of WithingsClient and WithingsUser

Store your client ID, client secret and redirect URI in variables. Then, 
create a new instance of WithingsClient

    my_client_id = "---"
    my_client_secret = "---"
    my_redirect_uri = "---"
    
    api_client = withings_client.WithingsClient(
        my_client_id,
        my_client_secret,
        my_redirect_uri)

If everything works fine, a data folder with your client parameters 
will be created. This file can be used to reuse the user client 
you created.

To create a new instance of WithingsUser, do the following:

    my_user = withings_user.WithingsUser(api_client)

Copy the authentication URL and paste it in your browser. 
Log in and copy the URL you are redirected to and paste it. 
If everything works fine, a user folder with a JSOn with your 
user parameters including your tokens will be created with which 
you can reuse it.

Your access token will be valid for 3h. After that, you can use 
your refresh token to get a new set of tokens.

    my_user.refresh_existing_token()

## General information about accessing data

### Date and time

* Sometimes, the Withings API expects date and time to be in unix format, 
and sometimes in human-readable format. To avoid confusion, the functions 
in this project always use unix format in the input parameters and convert 
it internally if necessary.

* Furthermore, be aware that the data which the Withings API returns 
sometimes includes the enddate, and sometimes not. 

* In some cases, startdate and enddate are mandatory, and in some cases, they are not. 
If they are not mandatory and you do not provide startdate/enddate, 
or if your requested data is too large (see pagination), sometimes the 
newest and sometimes the oldest data will be returned first. That holds because 
sometimes the sorting is ascending and sometimes descending.

* In some modules, date and time are relevant, in other modules only the date 
is relevant and if you enter date and time, the time will be stripped away. 

* If you provide the parameter `lastupdate`, only data updated after this date 
will be returned.

* In two modules, only the first 24h after the startdate will be returned if 
the difference between `startdate` and `enddate` is greater than 24h.

* The chunk size depends on the module and is between 200 and unlimited. The 
modules without a limit do not have an `offset` parameter.

* According to the Withings API Developer reference, there is no `offset` parameter 
for `sleep_summary.py` and I observed no `more` key in the returned dictionary. 
But according to my observation, the `offset` parameter is available and must 
be used if you want to get more than 300 rows of data.

* If `startdate` and/or `enddate` and/or `lastupdate` are required depends on the module.

### Pagination

For large amounts of data, Withings uses pagination, i.e. the data is provided 
in chunks. If more data is available than the chunk size Withing defined 
for the respective kind of request, the parameter `more` will be `True` and 
the `offset` parameter will be greater than `0` inside the initial request. 

Make another request with this integer as `offset` parameter 
without changing the other parameters. This will tell the Withings API how many 
data rows must be skipped to get the following chunk of data. It might be 
necessary to repeat this several times.

> [!WARNING]
> I observed inconsistencies in the pagination provided by the 
> Withings API. I noticed several times problems like the `more = False` or 
> `offset = 0` although more data was available. If you suspect that, it 
> might be a good idea to just try using an offset to see if there is more 
> data.

### Overview 

| name                        | type of startdate/enddate  | sorting | more than 24h? | chunks?   | `lastupdate`? | `offset`? | `data_fields`? | required parameters                                                 |
|-----------------------------|----------------------------|---------|----------------|-----------|---------------|-----------|----------------|---------------------------------------------------------------------|
| Heart Get                   | no date/time               | -       | -              | -         | -             | -         | -              | `signal_id` as only parameter                                       |
| Heart List                  | date with time             | desc.   | yes            | 200 rows  | no            | yes       | no             | nothing, without parameters newest data will be returned            |
| Measure Getactivity         | date without time          | asc.    | yes            | 200 rows  | yes           | yes       | yes            | either pair `startdate` + `enddate`, or `lastupdate`, but not both  |
| Measure Getintradayactivity | date with time             | asc.    | no             | no chunks | yes           | no        | yes            | `startdate`, or `enddate`, or both                                  |
| Measure Getmeas             | date with time             | desc.   | yes            | 4096 rows | yes           | yes       | yes            | nothing, without parameters newest data will be returned            |
| Measure Getworkouts         | date without time          | asc.    | yes            | 300 rows  | yes           | yes       | yes            | nothing, without parameters oldest data will be returned            |
| Sleep Get                   | date with time             | asc.    | no             | no chunks | no            | no        | yes            | both `startdate` and `enddate`                                      |
| Sleep Summary               | date without time          | asc.    | yes            | 300 rows  | yes           | yes (!)   | yes            | either pair `startdate` + `enddate`, or `lastupdate`, but not both  |

## Accessing data

Accessing data works like that (using Get Activity as an example): First, create the data for the 
request, and then send the POST request with this data and the instance of WithingsUser created above.

    now = dt.datetime.now() 
    two_weeks_ago = now - dt.timedelta(weeks=2)
    now = int(dt.datetime.timestamp(now))
    two_weeks_ago = int(dt.datetime.timestamp(two_weeks_ago))
    
    data = measure.data_measure_get_activity(startdate=**two_weeks_ago**, enddate=now, data_fields="steps")
    
    measure_dct = measure.post_request_measure(data, my_user, to_json=True)

## Working with the data

The data from the WithingsAPI are nested dictionaries. To work with them as Pandas dataframes, 
they need to be flattened. This can be done with the functions in the `api_data_utils.py` module.

    df = api_data_utils.dict_to_pandas_df(measure_dct)
