# VorratsDatenSpeicherungDB

**Knowledge thus far:**
EVA number is the unique trainstation number. Trains have a unique identifier.

Dataquality is horrible in this project for two reasons. 
1. All api output information is stored in XML attributes of elements rather than in the elements themselves.
2. All information is pulled from a relational database with very little documentation regarding the api calls themselves. Resulting in a terrible mess of an XML output.

Solution for this: Fully flattening all output XML and loading it into a Pandas Dataframe. I sincerely thank all the random stackoverflow threads and especially the creator of the "pandas read xml" package. You saved me from having to write a parser which would have cost me an awful lot of time and caused me a lot of stress. 

Next Steps:
1. Do some basic tests to absolutely ensure that the dataframe has the right structure and then name the Columns properly so that humans can grasp tf is going on. (Also delete output.txt after dataframe creation. It's already annoying) - Mostly done.
2. Split the dataframe into several and store them in defined folders. - Done
3. Import into SQL server (and figure out how to import at regular intervals) - This is proving to be harder than I expected because of course it is. At first I wanted to use merge. That wont do. I will be stealing from SO next I guess.
4. Do some fancy R stuff
5. Figure out how on earth to get this all onto the internet.
6. Find a way to not get broke due to server costs with this project. I swear this will be an issue. - Done, google gives 300 bucks.