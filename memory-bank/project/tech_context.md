# Technical Context: Expense Report Application

> **NOTE**: This is an example and should be updated for your application

## Frontend Technologies

- React 18 (`react@^18.2.0`, `react-dom@^18.2.0`)
- AWS Amplify UI React (`@aws-amplify/ui-react@^6.5.5`)
- AWS Amplify JS (`aws-amplify@^6.6.6`, `@aws-amplify/storage@^6.8.4`, `@aws-amplify/auth@^6.12.4`)
- Sentry for error monitoring (`@sentry/browser@^9.10.1`, `@sentry/react@^9.22.0`, `@sentry/replay@^7.120.3`, `@sentry/tracing@^7.120.3`, `@sentry/vite-plugin@^3.2.4`)
- ai SDK from Vercel (`ai@^4.3.16`)
- js-cookie (`js-cookie@^3.0.5`)
- jwt-decode (`jwt-decode@^4.0.0`)
- XLSX for Excel export (`xlsx@^0.18.5`, `xlsx-js-style@^1.2.0`)
- Vite (`vite`, `@vitejs/plugin-react@^4.2.1`)
- TypeScript

## Backend Technologies

- Node.js (v20+)
- TypeScript
- AWS Amplify Backend (`@aws-amplify/backend@^1.5.0`, `@aws-amplify/backend-cli@^1.2.9`)
- AWS CDK v2 (`aws-cdk@^2.138.0`, `aws-cdk-lib@^2.138.0`)

## External Integrations

- OpenAI GPT-4 Vision API for receipt parsing
- AWS S3 for image storage
- JWT for authentication with existing systems

## Development Environment

- Recommended IDE: Cursor with TypeScript and React extensions
- Node.js v20+ required
- AWS CLI configured for deployment
- Git for version control

## Deployment Strategy

- Frontend: AWS Amplify Hosting
- Backend: AWS Amplify/AWS Lambda
- Database: AWS DynamoDB
- Storage: AWS S3

## Technical Constraints

- JWT integration with existing infrastructure
- Mobile-responsive design requirement
- Excel export format compatibility
- 10MB maximum file size for uploads
