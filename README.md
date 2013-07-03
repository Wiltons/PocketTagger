A Python script to tag articles in Pocket (http://getpocket.com) as 'short' or 'long' based on the wordcount of the article.

Thanks to tbunnyman for work on Pocket-Calibre plugin which I used as reference (https://github.com/tbunnyman/ReadItLater-Calibre-Plugin/)

List splitter unceremoniously plucked from StackOverflow (http://stackoverflow.com/a/752562)


Version 0.1
   * Hardcoded tags (short, very_long)
   * Hardcoded parameters for the length of a short or long article
   * Optional to only tag long or short articles
   * Splits modification URL to chunks if URL is too large (hardcoded at 50 items)

TODO:
   * Fix hardcoded variables
   * Smart tag based on length of articles previously tagged as 'X'
   * Fetch_item functions don't need so much information from the item
   * Proper error handling
   * OAuth?

