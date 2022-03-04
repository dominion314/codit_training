Hello IT breatheren, I am back with another video, thank you for joining me. Today I'm going to teach you how to do devops and in this video we're going to touch on a few things. We're going to review write some python code, create a schema template, and then compare a customer request against that template. Im sure this sounds complicated but its easily once we apply it practically, its actually a very straightforward process.

Simply, we're going to create a python script that reads a customer request for a new resource in the cloud and then ensures that it meets all of our code requirements. 

This video is not meant to be a stand alone lesson, but rather to provide you some insight into the work of a devops engineer. I'm going to explain things to the best of my ability, but I will be moving fast so if you're unsure about something, post your questions in the comments below.

Be sure to like this video and subscribe to the channel, and without further ado lets get started. 

-The first thing we want to do with any project we're working on is to state our objective:

We are basically validating a customers request for a new PSA. What is PSA? Private Service Access is basically a way for app developers to allow 3rd party businesses to access their data securely. So lets say theres an app developer creating an app that allows for self-checkout in your store. However, in order to do so he has to expose customer data to a 3rd party that just happens to be from China. Of course they're a totally honest and trustworth business partnet, but why even take the chance of leaking customer data? Thus we introduce PSA as a resource within the cloud that can give this Chinese company only to the app developers data and NOTHING else within the IT department. 

By creating this script and the schema parameters, we protect our source code and are able to save the company money b streamlining the deployment of this PSA and getting it right the first time.

So essentially, our goal is to write a script that will review a customer request for PSA and ensure it meets our code/secuity requirements. This is a very typical workflow in devops, to write  policies that protect our source code and make these requests easily repeatable.  

-Let start off by writing our python script. We will be using a very useful library known as cerberus, which I will post in the description below. 
-Now lets create the schema tempalte that will serve as a checklist for our rqeuirements. Before we do though, What is schema? Schema is term we use to describe the validation of data types. Basically schema outlines what words, letters, characters, and symbols are allowed within a request. For example, if a customer has a typo in their request that leaks customer data, we want the schema to catch the error. Because the schema template is mirroring the customer request , we will need to use it as a reference. For the sake of time I've already written the customer request and schema template, so lets take a look.

Ideally we would want them to only have to fill in their team name and the subnet they need.

-Breifly discuss PSA connecting to our mongo DB.
-Pass the MR
-Fail the MR
-Pass again

As you can see devops covers a wide array of different disciplines within IT. For my job I have to know a little networking, a little python scripting, and also YAML. However, one you understand the fundamentals all of those different areas are what produces the cloud landscape that we see today. With more businesses moving to the cloud, I can only imagine that demand for talented devops engineers is only going to increase. 

So I hope you enjoyed this walkthrough and the code for this video will be linked in the description below. Be sure to like and subscribe and as always, Ill see you in the next one!
