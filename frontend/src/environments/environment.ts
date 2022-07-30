/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'https://dev-4rza57yr.us.auth0.com', // the auth0 domain prefix
    audience: 'coffeeAPI', // the audience set for the auth0 app
    clientId: 'pv0ZhlFUosFwGAs01HJQ1Ymx1Z4T2GsA', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application. 
  }
};
