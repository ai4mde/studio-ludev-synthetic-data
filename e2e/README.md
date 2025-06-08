# End-to-End Testing with Playwright

## Setup Instructions

### 1. Install Dependencies

Navigate to the `e2e` directory and install the necessary npm packages:

```bash
cd e2e
npm install
```

This will install all the dependencies listed in the `package.json` file.

### 2. Build and Run Docker Containers

In another terminal, navigate to the directory containing your docker-compose.yml file, then build and start the Docker containers:

```bash
docker-compose build
docker-compose up -d
```

### 3. Create Class Diagrams in AI4MDE Studio

1. Open your web browser and navigate to the AI4MDE Studio web application.
2. Create the class diagrams using the tools provided in the AI4MDE Studio.

### 4. Update the Configuration

Update `/config/testConfig.js` to match the names of the project, system, and interface you have chosen.

## Running the Tests

To run the end-to-end tests using Playwright, use the following command:

```bash
npm test
```

To open the Playwright test report after running the tests, use:

```bash
npm run test:report
```

To open the Playwright test in headed mode, use:

```bash
npm run test -- --headed
```
