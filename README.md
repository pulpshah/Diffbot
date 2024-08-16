# Diffbot Documentation

# Overview:
Diffbot is a suite/collection of products that makes it convenient to find and use data from the web without having to structure or clean it from its original website markup form. 

For Pulp’s specific purposes, Diffbot will be used for reference extraction, which will allow a user of a product such as the USPDC to quickly request and receive a reference related to the part of text they inquire about.

# Products:

## Extract
Extract quickly categorizes a website into clean, structured JSON at less cost compared to traditional scraping methods.
Used when a developer needs to look through thousands of web pages and sites.
Most efficient when the URL to be used is already known.
Information that is extracted is stored in fields that can either be custom-made by the developer or are predefined by existing Extract APIs.
Existing Extract APIs include:
Analyze API, to be used when you need to determine what type of content is at your URL. Reroutes to the following APIs.
Article API, to be used when information is to be extracted from written content. Can extract authors, sentiment, comments, page URLs, etc.
Product API, to be used for information about products, including description, price, reviews, etc.
Image API, to be used for information about images, such as dimensions.
Video API, to be used for information about videos, such as dimensions.

## Knowledge Graph
A huge graph database of entities that has already been crawled through and structured.
An entity is a “thing” that populates the graph, which will have various characteristics and relationships to other entities. An entity can be a person, organization or place. Each has a unique identifier.
An ontology describes the types of entities and their relationships between each other. They can be accessed by seeing what fields can be tickled for each type of entity. 
Ontologies in knowledge graphs are flexible, and contain entities’ unique identifiers, which ensures that information can be updated quickly (important in the ever-changing modern world) and that coreference resolution is possible (determining whether entities with the same name are distinct/separate).
DQL (Diffbot Query Language) can be used to search the knowledge graph to retrieve information if they don’t specifically know the type of entity they’re looking for, and want to find all potential candidates.
A basic query requests the type of entity, followed by filters.
Nested queries help retrieve more specific information.
If the developer already knows what entity they’re looking for, Enhance API may be used to return even more information on that entity based on all that is available about that entity on the web.
Enhance API will score several candidates against the submitted query (the more identifiers in the query, the better) and then return the best matched candidate with corresponding extracted information.
Entities are queried as key-words or phrases rather than specific URLs (as in Extract).

## Bulk & Crawl
Crawl works with Extract by spidering through a site for links, and compiling them into a collection that can then be sent to Extract for processing.
Used when a developer does not yet have the URLs they want.
Bulk works with Extract by sending all the URLs submitted to it as a collection to Extract, after which data can be processed, downloaded or searched.
Used when a developer already has the (big) list of URLs needed.
DQL (Diffbot Query Language) can then be used to search a collection made by a Bulk or Crawl job.
Note: Not available for students accounts/start-up accounts under the Diffbot pricing plan.

## Natural Language Processing
Instead of using URLs, NLP will extract entities and data about them from raw text.
Specifically, NLP will extract the entity types sorted by their salience (whether they are the main point of the piece of text), sentiment (whether the text has a positive/negative attitude towards the entity), facts (pre-defined in schema of Diffbot), open facts (directly taken from text) and a knowledge graph.


## Accessing the APIs:
An API token is necessary to use Diffbot in any capacity.
Upon obtaining your token, declare it globally in your Python script:
diff_token = 'YOUR_TOKEN'
Import the “requests.exception” library and set up a global timeout variable. Diffbot APIs are expensive to use and you do not want to waste time and credits on calls that are taking too long to proceed.
time_out = 30 

Then, you can declare variables to hold the queries (for the Knowledge Graph) or URLs (for Extract) either globally or as part of a larger function. The “requests” library should be imported for convenience, since you will be accessing parts of the web. Most commonly, “objects” is the all-encompassing field that is returned by a json object extracted by one of Diffbot’s APIs, so you must check for it before proceeding to extract and return further fields.

## Example of a basic query to the Knowledge Graph:
def query_knowledge_graph(query):
diffbot_url= f'https://api.diffbot.com/v3/knowledgegraph?token={diff_token}&query={query}'
   try:
       response = requests.get(diffbot_url, timeout=time_out)
       response.raise_for_status()
   except (RequestException, Timeout) as e:
       print(f"Timeout error querying Knowledge Graph: {e}")
       return None


   data = response.json()
   if 'objects' not in data:
       print(f"No objects found for {query}.")
       return None
  
   results = data['objects']
return results

## Example of basic query with a URL to the Extract API (Analyze API is called by default by diffbot_url, since this will automatically redirect Extract to the proper API under its umbrella by URL type):
def access_extract(url):
diffbot_url= f'https://api.diffbot.com/v3/analyze?token={diff_token}&url={url}'
       try:
           response = requests.get(diffbot_url, timeout=time_out)
           response.raise_for_status()
       except (RequestException, Timeout) as e:
           print(f"Timeout error accessing Extract: {e}")
           continue


       data = response.json()
       if 'objects' not in data:
           print(f"No objects found for {url}.")
           continue


       results = data['objects']
return results


results[0].get[‘...’] can then be used to access specific fields within the returned json object. 

## Example code for returning the types (video, article, image, etc) of a list of URLS passed to Extract:
def ref_type(refs):
   ref_types = {}
   for ref in refs:
diffbot_url = f'https://api.diffbot.com/v3/analyze?token={diff_token}&url={ref}'
       try:
           response = requests.get(diffbot_url, timeout=time_out)
           response.raise_for_status()
       except (RequestException, Timeout) as e:
           print(f"Timeout error accessing type for {ref}: {e}")
           continue


       data = response.json()
       if 'objects' not in data:
           print(f"No objects found for {ref}.")
           continue


       results = data['objects']
       ref_type = results[0].get('type').lower() if results else 'NO TYPE'
       if ref_type:
           ref_types[ref] = ref_type
  
   return ref_types

## Further Reference:
https://docs.diffbot.com/reference/introduction-to-diffbot-apis
