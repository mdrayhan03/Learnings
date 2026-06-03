# The Client-Server Model
## What is the Client-Server Model?
The Client-Server Model is a foundational structural framework for distributed networks. At its core, it divides an application or system into two main components that communicate over a network:

1. The Client (The Requester): This is the front-end or user interface component. It does not contain the core application logic or primary data storage. Instead, it captures user input, formats a structured request, and sends it across the network. Examples include web browsers (Chrome, Safari), mobile apps, desktop applications, or even smart TVs.

2. The Server (The Provider): This is the backend component that manages resources, databases, and heavy computation. It remains in a listening state, waiting for incoming client requests. When a request arrives, the server processes it (e.g., runs business logic, queries a database) and returns a structured response to the client.

Communication between the two follows a strict Request-Response cycle: a client must initiate communication with a request before a server can reply with a response.

## Where is it Used?
Practically the entire modern web operates on this model. Anytime software requires centralized data storage, security, or shared access across multiple users, it employs a client-server architecture.

* Web Applications: Your web browser (client) requests an HTML page from a web hosting server (server).

* Mobile Apps: A ride-sharing app on your phone (client) requests nearby driver locations from the application's backend infrastructure (server).

* Databases: A backend application server acts as a client when it requests raw data tables from a centralized database instance like PostgreSQL or MongoDB (the database server).

* Cloud Storage: Desktop applications sync local files by uploading them via API requests to centralized cloud object storage servers.

## Why Is it Crucial for Architecture?
Before you can split an application's internal code into patterns like Hexagonal or Microservices, you must understand how code executes across physical or logical boundaries.

The client-server model teaches you about network latency, statelessness (each request must contain all the information needed to understand it), and the separation of concerns between user presentation and data management.

## Mini-Project: Raw HTTP Request Handler
To truly master this model, you should avoid high-level frameworks (like Express, Django, or Spring) that hide the network layer. Instead, you will build a minimal socket-level server that acts as the Server, and use a command-line tool or browser as the Client.

# Coupling & Dependency Injection
## What is Coupling?
Coupling refers to the degree of direct dependency between two code modules or classes.

- Tight Coupling (Bad Architecture): Class A knows exactly how Class B is built and works. If you change a single line or variable inside Class B, Class A breaks. The code is rigid, fragile, and almost impossible to unit test.

- Loose Coupling (Good Architecture): Class A knows that a component exists to do a specific job, but it doesn't know how it does it. They communicate via Interfaces instead of concrete classes.

## Real-World Analogy
Think of a wall outlet. Your laptop charger requires electricity, but it doesn't care if that power comes from a coal plant, hydro-electric dam, or solar panels. The outlet is an Interface. If your charger was hardwired directly into a specific power plant's generators, that would be Tight Coupling.

## What is Dependency Injection (DI)?
To achieve loose coupling, we use a technique called Dependency Injection.

A Dependency is simply an object that another object needs to do its job. For example, a UserController needs a DatabaseConnection to fetch a user.

- Without DI: Class A handles creating its own dependencies internally using the new keyword (e.g., this.database = new PostgreSQLDatabase()). This instantly hardcodes Class A to that specific database type.

- With DI: Class A does not create its dependencies. Instead, it declares what it needs (usually in its constructor), and some external force "injects" or hands those dependencies to it.

## Why Is it Crucial for Architecture?
In advanced architectural patterns, your core business rules must remain pure and independent of external tools.

- If you want to run automated tests, you can't have your code trying to connect to a live database. You need to inject a Mock/Fake Database.

- If you use Dependency Injection, your core application remains completely unaware of whether it's running in a production environment or a testing pipeline.

## Mini-Project: Swappable Notification Service
To see the power of loose coupling, you will build a small system where a core manager can switch out its entire notification infrastructure without modifying its own code.

# Layered (N-Tier) Architecture
## What is it?
Layered architecture breaks an application down into distinct, horizontal layers. Each layer has a highly specialized role and a strict rule: a layer can only talk to the layer directly beneath it. It cannot skip layers, and lower layers cannot initiate communication with upper layers.

While you can have any number of layers (hence "N-Tier"), a standard 3-Layer backend application consists of:

1. The Presentation / UI Layer (Controllers): 

    - Role: The entry point of the application. It handles incoming network requests (like HTTP GET/POST), validates user input formats, and returns the final response (like JSON or HTML).

    - Rule: It must never talk to the database directly. It simply passes the sanitized input down to the business layer.

2. The Business Logic Layer (Services):

    - Role: The "brain" of your application. This is where your actual application rules live (e.g., calculating discounts, validating if a user is old enough to register, processing a ride-booking math calculation).

    - Rule: It knows nothing about HTTP, request parameters, or database connection strings. It acts on pure data given to it by the Controller and asks the Data layer to save/fetch things.

3. The Data Access Layer (Repositories / DAOs):

    - Role: The data gateway. This layer contains raw database queries (SQL, ORM calls like Django/SQLAlchemy models, or NoSQL queries).

    - Rule: Its sole job is to fetch records or save them. It does not make executive decisions about business rules.

## Why Use It?
- Maintainability: If your database schema changes, you only update code inside the Data Access Layer. Your Presentation Layer remains entirely untouched.

- Readability: New developers instantly know exactly where to look for a specific bug based on what type of issue it is.

## Mini Project: E-Commerce Product Catalog
Let's put this into practice. You are going to build a mini-backend engine for an e-commerce catalog following strict horizontal layers.