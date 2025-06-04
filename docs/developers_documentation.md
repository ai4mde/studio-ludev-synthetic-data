# AI4MDE Developers Documentation
This guide outlines the key structure and logic behind AI4MDE, specifically aimed at developers focusing on the prototype creation and synthetic data generation.


# Frontend


## File Structure & Component Overview

Most relevant logic for prototype creation is located in:

`$lib/features/prototypes/CreatePrototype.tsx`

This React component is responsible for rendering the modal interface that allows users to generate Django-based prototypes with synthetic data (or without).

## Component Functionality

### 1. Opening the Modal

- The modal is controlled by a global atom (`createPrototypeAtom`).
- The `Modal` component displays a dynamic form for prototype creation.

### 2. Data Fetching

- System metadata (interfaces and diagrams) is fetched via:
  - `useSystemInterfaces(systemId)`
  - `useSystemDiagrams(systemId)`
- A database hash is computed using `CryptoJS` to track the current schema state.

### 3. Prototype Submission

- Upon submitting the form:
  - Metadata is compiled (including interface selections, diagram structure, and synthetic data flags).
  - A `POST` request is made using `authAxios` to the backend to initiate prototype creation.

## Synthetic Data Generation (Frontend)

To access the synthetic data toggle, the user first clicks the “Generate Prototype” button in the AI4MDE interface, which opens a modal form. This form gathers basic information like the prototype name, description, and selected interfaces. As the user scrolls down the form, they encounter the “Use Synthetic Data” toggle. Once enabled, it triggers another popup where the user can input how much synthetic data to generate and optionally add custom instructions.

### Toggle Control

The user can enable synthetic data generation by toggling the "Use Synthetic Data" switch in the prototype creation form. When toggled on, it updates the `useSyntheticData` state and opens a secondary modal for further configuration.

### Configuration Modal

In the modal, users can specify how much synthetic data they want to generate. They can enter a global row count for all tables or provide per-node row counts. Additionally, optional custom instructions can be set for each node. These inputs are saved in `syntheticCounts` and `syntheticInstructionsPerNode`.

### Data Validation

Before submission, the frontend checks for relationship constraints like one-to-one, one-to-many, or many-to-one. This is done using the `getMultiplicityRules()` and `handleSyntheticValidation()` functions to ensure that user input respects the schema’s cardinality.

## Submission of the Form

When the user submits the form, a metadata object is sent to the backend. This object includes settings such as whether authentication and synthetic data are enabled, the number of rows per table, any global or per-node instructions, and the system’s diagrams and interfaces. This ensures the backend receives the full context to generate meaningful synthetic data using a large language model (LLM).



# Backend

## **File Structure & Component Overview**

The backend code for prototype generation is located at `prototypes/backend/generation/generation_scripts/generate_synthetic_data.py`

As outlined in `architecture.md`, The other components of AI4MDE interact with the prototype generation container through a Flask API at `/prototypes/backend/api.py`. Within the _generated_prototype_ endpoint of the Flask API the control flow is redirected to the generate_synthetic_data.py script if the metadata of the POST request to _generate_prototype_

indicates that the user had toggled synthetic data generation in the form.

When the generate_synthetic_data.py is called, a functional Django project with a shared models app should already be instantiated by the generation architecture. See architecture.md > Prototypes > Generation architecture for more information. The name of the project as well as the name of the system where the project resides are passed to the synthetic data generation script.

The synthetic data generation script infers the UML class diagram that the user has designed from the generated Django application, and does not rely on the metadata passed to the _generated_prototype_ endpoint for this. To the contrary, the amount of records to generate per class, whether synthetic data generation is enabled and potential extra context for the LLM are taken from the metadata.

## **Component Functionality**

- The generated Django prototype is initialized in setup_django(), based on the app’s name and system name that are passed to the script.
- Model definitions are extracted from the generated shared models app, in extract_model_definitions(). The shared models are read out one by one and stored in a JSON format to encourage the LLM to return data in a consistent format that can be parsed.
- Based on the extracted model definitions and the metadata provided by the user, a prompt is constructed in make_prompt()
- The LLM response is parsed into a JSON object.
- Before the models can be saved into the Django application, the models are sorted topologically based on foreign key constraints. Django will throw an error if an instance with empty foreign key fields is attempted to be saved to a model that is defined as having foreign keys.
- The synthetic data is saved per model, in topological order. While saving the data, the fact that primary keys generated by the LLM may not align with automatically assigned primary keys in Django is kept in mind. For every model a dictionary is kept that maps the LLM generated primary key to the actual primary key. This is necessary because models with foreign keys refer to foreign instances through their actual foreign key and not the LLM generated foreign key.

Note: as of writing this documentation, one-to-one and one-to-many UML associations have been implemented for prototype generation.
In the case of one-to-one associations, the foreign key constraint is placed on the Django model representing the "source" class. For one-to-many associations the foreign key constraint is placed on the Django model on the "many" side of the association.

## **A possible direction for further development**

While developing the current system the choice was made to generate the entire synthetic database in one joint prompt. The reason for this choice was that an LLM can easily create coherent connections between related classes in one prompt.

This approach does have its limitations. Open source models in Groq seem to struggle with generating large amounts of data at once (In the order of 10 tables with 20 records each).

The model output either decreases in creativity i.e. Person1, Person2, … Person20. Are generated instead of actual names. Or the model outputs less data than is asked.

A potential solution would be to let the LLM generate the data per class rather than for the entire database. This solution would bring its own complications with it. More prompt engineering would have to be done to ensure that at the time of generating the first class in topological order the structure of the entire UML class diagram is known to the LLM such that it can still create coherent connections. Furthermore, a history of relevant already generated data would have to be passed per class in order for the LLM to generate coherent connections.

Another possible way forward is to let the user regenerate specific classes. The user should be able to select classes for which the LLM did not do a good job. A separate interface in the studio frontend for generating data would probably improve the end user experience since generating an entire prototype to try out synthetic data generation each time will get tedious due to the waiting time involved.
Footer

