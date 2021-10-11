Once you've added documents to you're ready to start searching!

lnx provides you with 4 major ways to query the index:
- `normal` The tantivy query parse system, this is not typo tolerant but is very powerful for custom user queries, think log searches.
- `fuzzy`* A fuzzy query, this ignores the custom query system that the standard query parser would otherwise handle, but intern is typo tolerant.
    *  if you have `use_fast_fuzzy` set to `true` for your given index this will
use the fast fuzzy system. 
- `more-like-this` Unlike the previous two options this takes a document reference address and produces documents similar to the given one. This is super useful for things like books etc... Wanting related items.
- `term` expects the exact value in the query without any fuzzy matching or parsing like `normal`
