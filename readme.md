Data Requirements:

1. daily prices (for all cryptos)
2. 24 hour volume (for all cryptos)
3. marketp cap (for all cryptos)

Data Pipeline Artifacts:
Docker Containers:

1.  db
    - manages the mysql database instance
    - path: .//coingecko/docker/db
2.  app
    - manages the python scripts that pulls and loads data from the api and database.
    - contains the shell script to run the python scripts
    - path: ./coingecko/docker/app/src/

Architecture:

The approach I have decided to take with the project is to utilize docker and python to create
simple etl pipeline that will extract data from the coingecko api and load it into a mysql database.
I decided to leverage existing python modules to similty the pipeline (sqlalchemy and pycoingecko)
The sqlalchemy python is an ORM that allows for an interface to a realtional database, and the pycoingecko is a api wrapper for the coingecko api. By using the latter, the complexity of the architecture can be reduced by not having to create these modules that perform the similar funcitonality.

The infrastruce I selected to use for this project is docker, mysql, python, crontab. By using docker to containerize the data pipeline, we can create separate logics for the serparate functions of the pipeline. In this project i decided to use two separate containers, one for the mysqldatabase, and another for the python application. The pipeline orchistration and schedule is
implemented using a shell script and crontab. The shell scirpt contains the commands to exeuctre the desired python scripts to run the pipeline. There are three main components to the python scripts,
the db setup script, the assets script, and the prices script. The db script sets up the tables
in the database. The asset script pulls the list of assest from coingecko and then upserts the data to the asset table in the database. The prce script pulls the data from the id values in the asset table and then makes a request to the coingecko api to retrive the price data for those assets, and then inserts that data into the price table.

Once I finalized the data pipeline with the above data architecture, I did not have a lot of time to run the pipeline for period of days, so I had to opt to run the pipeline in hourly intervals to demonstrate and collect data successfully using the pipeline. I ran the pipeline artifacts on an ec2 instance.

I also opted to perform limited transformations on the data since the dataset, with the idea of letting the database handle and python scripts handle the data types and uniqueness of the records being inserted into the tables. For example, by using the python ORM we are able to define the datatypes of the table columns, which creates a implicict check for the data being inserted to the table. In addition, the unqueness and duplication of data is also managed by the table schema, for instance, by setting the primary key of the table to the id we receive from coingecko the table will enforce that the column will be unique, otherwise the record in the table will be updated if that id appears again.

Extensions of the pipeline can be made by creating new python script and including the into the shell script that is being executed by the crontab. For example, additional validations and transformations may be incorporated into
the pipeline be addding then in the order the python scripts should be executed, such as creating an aggregate table that rolls up price data to specific time intervals (hourly or daily), or make additonaly computations on the price data that could be done in an additonal transformation script.

In regards to extending the pipeline with additional data sources, depending on the context and data sources, additional tables may be added to the table. or a new schema with the same tables may be created in order to consume data from an additional cryptocurrenty price aggregator api. And the similar pipeline may be used with extending the data sources ingested. If the additional source are outside of coingecko, and the data source does not provide an api wrapper, it will be benedifical to write a custon api wrapper that uses an http library, like requests to pull data from the api.

The soltution implemented in this projects lends itself to similicity, but if scaling is the goal, then investing more in the infrasructure will be important piece of the pipeline. A solution like airflow or aws step function would be useful for productionalizing and scale the data orchestration engine. The compute engine will also be important when scaling the pipeline. Docker container could be ran on kubernetes or ECS, or lambdas could be used to execute the python code. Additionally, if there are large batches of data to be processed spark can be utilized for large batch jobs.
