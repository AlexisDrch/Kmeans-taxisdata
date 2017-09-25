# DataWarehouse   |   Theory   ,   Optimization   &   Implementation NF26   

Credits:   6 Lectures   hours: 2h/week Projects   hours: 2h/week
One project (25%), two written exams (first one 25%, second one 50%)
Prof.   Pierre   Morizet-Mahoudeaux -  2017-2018

## Course   Overview


This course aims at presenting the principles of tools development and using for data warehouse conception and decision taking with specific   tools   (Business   Objects,   regression,   segmentation).
The class NF26 aims at presenting the data warehouse construction principles, with an introduction   to   NoSQL.
In this class, a first part is focused on the major concepts related to data warehouses. The students learn how to analyze “clients” needs and requests so as to conceptualize an architecture that will answer those needs in an optimal, simple and ready to use way: the data marts.  In this part, the differences, pros and cons of different data warehouse models are emphasized.
In order to conceptualize a data warehouse, the students learn to  separate business process data into facts, holding measurable and quantitative data about a business, and dimensions which are descriptive attributes related to fact data. Examples of fact data include sales price, sales quantity, and time, distance, speed, and weight measurements. Related dimension attribute examples include product models, product colors, product sizes, geographic locations,   and   salesperson   names.
Main theory of the first part includes the following keywords:  dimensions tables - facts tables -    hierarchy   -   normalization   -   denormalization   -   star   schema   -   snowflake   schema.

In a second part of this class, students learn a new paradigm for data warehouse implementation and conceptualisation : NoSQL. Using Cassandra technologies and Python as main programming language, students implement a complete data warehouse following NoSQL   and   column   table   logic.
In this project the students will take advantage of Cassandra model for presenting a dataset in a way that is interesting for analytics, data visualisation and that allows non-technical people to   retrieve   and   get   real   business   value   on   top   of   the   row   data   set.
Main theory of the second part groups the following keywords:  Cassandra - CAP Theorem - Eventual consistency - NoSQL - Consistent Hashing - Nodes - ACID and BASE - Analytics - Kmeans.

## Project   Description

#### 1.
As a first project, students have to implement the process of parsing, cleaning and injecting data in a data warehouse. Hence, following a customer request, row data are modified and structured   accordingly   using   Pentaho   software.


#### 2.
The second and main project of the class consists in implementing a NOoQL data warehouse with Cassandra technologie. Based on an open-source data set provided by a taxi company in Porto (Portugal) students have to imagine clients requests and build the according datamarts and fact tables. On top of the data warehouse, students have to think about analytics that would provide business values and implement the K-means algorithm in Map Reduce to detect   patterns   and   classes   in   the   taxi   trip   dataset.



