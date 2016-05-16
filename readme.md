# Shopify ETL

<img src="https://circleci.com/gh/datamafia/ShopifyETL.svg?style=shield&circle-token=:circle-token" alt="Build Status"/>

ShopifyETL provides a toolkit for extraction of data into an object as well as written JSON files. The transform and load duties specific to each Shopify use case, so you will need to write that part or hire me (_emoticon_). 

```ShopifyETL``` is not limited to extraction of information and a tool kit for adding transformation and loading of Shopify data. Also included is low level API functionality that will speed up development work using the Shopify API and Python. The basic tools available are of huge potential, for example:

* All calls to Shopify for any Python application can take advantage of the ```Shopify``` class.
* The extraction provides the ability to perform content and shop audits with ease.
* The verbose and plentiful logging, logs, and file writing capabilities are a key accounting tool for large operations.
* The foundation of this package aims to integrate with queueing systems as well as big data processes.
* The operations, patterns, and code presented in this package is ready for cron-tab integrations to perform what ever special magic you may need (like daily sales reports tailored to your teams needs).

<a href="#myPackage">_Why not the existing Shopify API package?_</a>

Requirements:

* Python 2.7.x (will port and test on Python 3 #helpWanted)
* Python [Requests Library](http://docs.python-requests.org/en/master/) 
 * To install ```pip install -r requirements.txt```

Also important, this program includes Shopify 429 monitoring and a built in and configurable ```sleep()``` respecting the API limits. Due to the long running nature of many operations it is not advised to run the this in a production environment where resource blocking is a concern.

# General Operation

In normal operation the pattern is simple, classes are all extended in a logical manner with key properties available to customize the experience.

### Subclassing

The ```ShopifyCreds``` class is extended by ```Shopify```. Job type classes then extend ```Shopify```. Each of these classes (or type of class) have a discrete and specific role.

A "job type" class is a subclass of ```Shopify``` and does all of the actual work in the final application or destination. ```ShopifyETL``` ships with "job type" classes ready to Rock-n-Roll, they are mysteriously located in the ```jobs``` folder and used in ```run.py```.

### ShopifyCreds class

Location: ```shopifyETL/shopify_creds.py```


```ShopifyCreds``` imply holds the credential information for use in the greater ```Shopify``` class. There are 4 key properties.

* ```SHOPIFY_KEY```: Shopify API key.
* ```SHOPIFY_PASSWORD```: Shopify API password.
* ```SHOPIFY_STORE```: Shopify API "store" such as ```myshop``` in ```myshop.myshopify.com``` when acting as admin.
* ```SHOPIFY_BASE_URL```: Shop url, can be a ```myshopify``` url such as ```somestore.myshopify.com``` or a custom domain name. (should not contain "http://", just sub/domain.something)
* Not key, but still used in subclasses ```overwrite_files``` is a global flag for overwriting files in the jobs. 

It is a personal preference to use an object for credentials. The cleanliness in code, discoverability in IDEs, and certainty in debugging is welcome.

####Usage:

With the ```config.cfg``` file available with valid credentials:

```
cred_obj = ShopifyCreds()
```

Passing in credentials via a dictionary and ignoring the ```config.cfg``` file:

```
creds = dict(
    SHOPIFY_KEY='abc',
    SHOPIFY_PASSWORD='def',
    SHOPIFY_STORE='ghi',
    SHOPIFY_BASE_URL='jkl',
)
cred_obj = ShopifyCreds(creds)
```

### Shopify class

Location: ```shopifyETL/shopify.py```

Extends: ```ShopifyCreds```

The ```Shopify``` class is a base class for all underlying operations. Simply put, this class extends __GET__, __POST__, __PUT__, and __DELETE__ functionality of the requests library for connecting to Shopify in a sane, understandable, and consistent manner.

####Usage:

Using the ```cred_obj``` created by the ```ShopifyCreds``` class:

```
s = Shopify(cred_obj)

# or in a more compact manner

s = Shopify(ShopifyCreds())

# also compact but using a dictionary for credentials

s = Shopify(ShopifyCreds(creds))
```

The ```Shopify``` class handles all of the basic API connectivity as well as [429](https://help.shopify.com/api/guides/api-call-limit) error handlers (a work in progress), plus other low level tasks.

####A few methods filled with intrigue...

```get_connection()``` returns the connection string template. Use this any time you want the connection string or as needed in subclasses. The Shopify address to make API calls follows this pattern

>https://```SHOPIFY_KEY```:```SHOPIFY_PASSWORD```@```SHOPIFY_STORE```.myshopify.com / ```call``` / ```optional params```

Also returned in the connection string from ```get_connection()``` is an additional (Python) ```/%s``` used for the addition of the API call.

```
https://abc:def@ghi.myshopify.com/%s
```

### Job Type Classes

Location: ```shopifyETL/jobs```

Extends: ```Shopify```

"Job Type" classes are the actual workers. Included with ```ShopifyETL``` are the following "Job Type" classes:


* <a href="#ExtractCollectionData">```ExtractCollectionData```</a> extracts collection information.
 * Location: ```shopifyETL/jobs/collections```
*  <a href="#ExtractProducts">```ExtractProducts```</a> extracts product information.
 * Location: ```shopifyETL/jobs/products.py```

Job classes by nature are long running operations. To extract data making multiple calls is usually required, pagination of API data is assumed, and various other gotchas are ready to break up the party. (such as rate limits).  

####Pattern and Abstract

System memory and local storage are two areas of concern.  Large operations on constrained machines will only cause problems. Unnecessary file writing to ethereal systems, writing of core store data, or exceeding storage allocation are legitimate concerns. Beyond these obvious problems ```ShopifyETL``` aims to be queue friendly highly compatible and available for large data operations. 

####Job Class Properties

* ```sleep_interval```: Second between page calls. 
 * Default is 1 second.
* ```page```: Starting page when pagination applies. 
 * Default is 1
* ```limit```: Page size (item count). 
 * Default 20
* ```chunk```: Boolean to control how files are written.
 * Default is ```False```, files will be written once all pagination is complete.
 * When set to ```True``` each page (per ```limit``` setting) of data is written to a JSON file instead of one larger file
* ```less_memory```: Boolean to control memory use.
 * Default is ```False``` and a list of results will be returned,
 * When set to ```True``` a list will  not be returned and results will not be kept in memory.
 
Each method performing operations extracting data has an argument ```write``` with a default to ```True```. If set to ```False``` no files will be written from this operation. When creating custom jobs feel free to use these ideas as necessary.


## Copy+Paste

Get a usable Shopify object with ```config.cfg``` used for credentials:

```
s = Shopify(ShopifyCreds())
print(s.get_connection())  # reflects the data in config.cfg
```

Get a usable Shopify object passing in a custom credential dictionary for credentials:


```
creds = dict(
    SHOPIFY_KEY='abc',
    SHOPIFY_PASSWORD='def',
    SHOPIFY_STORE='ghi',
    SHOPIFY_BASE_URL='jkl',
)
s = Shopify(ShopifyCreds(creds))
print(s.get_connection())  # https://abc:def@ghi.myshopify.com/%s
```

####Get (All Smart Collection) Data

See the ```run.py``` file for more examples. In general all procedures look like the following example.

```
from jobs.collections import ExtractCollectionData

col = ExtractCollectionData(ShopifyCreds())
smart_collections = col.extract_smart_collection_data()
```

####Chunking

To chunk the written data simply change the ```chunk``` property of the job class.

```
col = ExtractCollectionData(ShopifyCreds())
col.chunk = True
# col.limit = 1  # 1 item per page, good for testing otherwise a bad idea
smart_collections = col.extract_smart_collection_data()
```

#### No Memory

All of the operations append results to a base list. If you don't need this list of data or want to save memory the ```col.less_memory``` property needs to be changed.

Please note that a ```logging.warn()``` message will be issued because ```ShopifyETL``` counts the results available before the extraction and then the number of items in the aggregated list. If the list is not populated the final 

```
col = ExtractCollectionData(ShopifyCreds())
col.less_memory = True
# col.limit = 1  # 1 item per page, good for testing otherwise a bad idea
smart_collections = col.extract_smart_collection_data()
print(smart_collections)  # None

# Note a error will be issued:
# WARNING:root:Collection starting count (xyz) != number of results pulled from the API (0).
```

#### Granular Write Control

Using the boolean ```write``` in a method controls write (to file) on a per method level. The localized ```write``` boolean only effects the write for the method. To be clear, the default is ```True``` and setting to ```False``` will turn off writing of data to the local file system.

## ExtractCollectionData <a name="ExtractCollectionData"></a>

* ```extract_custom_collection_data()```: Custom collection data.
* ```extract_smart_collection_data()```: Smart collection data.
* ```extract_collect_data()```: Collect data.

## ExtractProducts <a name="ExtractProducts"></a>

* ```extract_product()```: Product data.


## Why not existing Python Packages<a name="myPackage"></a>

I am vary familiar with all of the various packages on the market. Philosophically there is an effort to minimize use of 3rd party software and packages. Some of these packages may solve __your problem__ better and that is okay. They did not speed up my development and only hindered my quality and speed.

It should be noted that the Requests library is a staple for Python and I appreciate the work and quality. Requests merely standardizes web connectivity. In reviewing various packages the "all things to all people" brings bloat and unnecessary complexity often via feature creep.

By contrast ```ShopifyETL``` is more resistant to feature creep by encouraging highly abstracted and almost entirely decoupled work via the ```jobs``` directory and subclassing. The ```ShopifyCreds``` and ```Shopify``` classes are stable, having been in use for well over a year in my own development.

The assumption is that a user of this package has probably built APIs, most probably has Requests already installed, used many APIs, knows the various ```URL``` libs, and has a distinct idea of what they need to get done. The user story for this package is:

* User knows how to build API calls
* User knows how to parse data
* User knows Python
* User knows the Shopify API well
* User knows how to handle exceptions, timeouts, and other issues and probably already has a system in place (possibly inherited from a greater framework).

To add bloat is not in my nature. Exceptional software is a product of knowing all your code, not "black box" middle ware. 

The ```ShopifyETL``` library is drop-dead-simple. The pattern for use is:

* Find the call I need to make via the docs.
* Format the ```call``` and ```data```
* Make the call via ```ShopifyETL```:

```
s = Shopify(ShopifyCreds())
results = s.shopify_post(call=call, data=data)
# so as you need w/results
```

No need to learn how someone mapped data to an ORM. No need to have all of the possible API calls "pre-mapped" waiting for a catastrophic failure when the API changes a little. No need to introduce another framework into what are commonly already complex systems. All I care about is the ```call```, ```data```, and the ```response/results```.  

>Simplicity is the most difficult solution of all, be ready to embrace it when found.


##License


Author: ```datamafia.com```

License: [MIT](https://opensource.org/licenses/MIT)

Copyright (c) 2016 @datamafia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
