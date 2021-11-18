# 4111Project

PostgreSQL account: njd2135
URL of our application: http://35.243.181.172:8111/

### Description:

In this part of the project, we've implemented almost all of the functionality that we'd specified in the initial project proposal. The user is able to input their fssn and get a list of their fish friends, types of predators, and current aquarium of residence. Users can “friend” other fish, creating a relationship between them and the friended fish. We tweaked one thing: instead of recommending an aquarium based on the type of fish the user is, the application instead shows tanks that exist in the same aquarium (with their ratings), so that fish can move in between tanks in the aquarium. We figured that a move within an aquarium would be more useful to the fish than a move between aquariums.

In addition to the features mentioned above, we also allow the user to input their fssn and get a list of their family, information about their owner, and their origin. Fish are also able to find the best owners in their country (with ratings above average), find the addresses of other fish, and find friends of friends that they aren't friends with yet (as a list of suggested future friends.)

### Note:

We know that we haven't fixed our SQL schema, based on the feedback you gave in Part 2 (for the lives_in constraint). Apologies; by the time we realized the magnitude of the changes we needed to make (delete a table, add more data to the fish table), we had already written all the SQL queries and didn't have enough time to safely make the change. We understand that we'll lose points for this, but we figure that a working application with a slightly incorrect schema is better than a not-working one with the right schema.

### Most interesting webpages

The most interesting pages we have (in terms of the most interesting database operations) are the bestOwners page and the suggestedFriends page. 

The bestOwners page is used to determine all owners that are above average in a given country; the page takes in a country string (i.e. Australia), and uses it to complete an SQL query that compares every owner (that owns a fish in the specified country) with the average of all owners who own a fish in the specified country. We thought this was a particularly interesting database operation because it required aggregation and joins between 4 different tables.

The suggestedFriends page is used to display friend suggestions for the user; specifically, it finds the friends of the user's friends that aren't already in the user's friend list, and displays those fish. The page takes in the fssn of the user, then performs the operation and displays the results in a list. The database operation, once written, isn't incredibly complicated, but we felt that it was an interesting database operation because of the duplicates that we had to take into account; one, the query had to remove all fish that were already in the user's friend list (which we did with an EXCEPT), and two, the query also had to remove the user themselves (something that I didn't account for originally; a fish's friend's friends includes the original fish, unless otherwise specified).