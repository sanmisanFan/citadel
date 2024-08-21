# Research Reviewer Project


* Automated static checks for thorough and consistent pre-review. 
* Visualization-supported peer review.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Introducation - FanL
The frontend of this project is build based on React + Antd UI framework. Citation_Stacking/ folder contains all the scripts from Akshit.

## Getting started
Do I run the front-end after the python processing scripts?

```
make run
```

## PDF Statistical Test Validator

This project converts PDF files to text, extracts statistical test results (F-tests, t-tests, and Chi-square tests), and validates the reported p-values.

```
make statcheck
```

To use the script, simply provide the path to a PDF file. The script will extract the text, find statistical tests, and validate the p-values.

```
pdf_path = 'path/to/your/pdf/p4045.pdf'
process_pdf_file(pdf_path)
```


## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `yarn test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.