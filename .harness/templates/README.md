# Harness Step Templates

This directory contains reusable step templates that demonstrate Harness's templatization capabilities.

## Available Templates

### 1. Run Pytest Tests (`run-pytest-template.yaml`)
A reusable template for running Python pytest tests.

**Features:**
- Installs dependencies from requirements.txt
- Runs pytest with verbose output
- Configurable test file (defaults to test_app.py)
- Sets PYTHONUNBUFFERED for better logging

**Usage in Pipeline:**
```yaml
- step:
    name: Run Tests
    identifier: run_tests
    template:
      templateRef: run_pytest_tests
      versionLabel: v1
```

### 2. Docker Build and Push (`docker-build-push-template.yaml`)
A reusable template for building and pushing Docker images.

**Features:**
- Configurable Docker connector
- Configurable repository name
- Automatic tagging with pipeline sequence ID
- Configurable dockerfile path and build context

**Usage in Pipeline:**
```yaml
- step:
    name: Build and Push
    identifier: build_push
    template:
      templateRef: docker_build_push
      versionLabel: v1
      templateInputs:
        type: BuildAndPushDockerRegistry
        spec:
          connectorRef: <+input>
          repo: myusername/myrepo
```

## Benefits of Templates

1. **Reusability**: Use the same step across multiple pipelines
2. **Consistency**: Ensure standardized practices across teams
3. **Maintainability**: Update once, apply everywhere
4. **Version Control**: Track template versions over time
5. **Input Parameters**: Make templates flexible with runtime inputs

## Example Pipeline

See `templated-pipeline.yaml` for a complete example of a pipeline using these templates.

## Importing Templates to Harness

1. Go to Harness UI → Templates → Step Templates
2. Click "New Template" → "Import From Git"
3. Select your repository and the template YAML file
4. Save and version the template
5. Reference it in your pipelines using `templateRef`
