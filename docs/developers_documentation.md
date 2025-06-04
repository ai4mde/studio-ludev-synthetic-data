# AI4MDE Developers Documentation

This guide outlines the key structure and logic behind AI4MDE, specifically aimed at developers focusing on the prototype creation and synthetic data generation.

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
