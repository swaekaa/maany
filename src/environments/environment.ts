export interface Environment {
  production: boolean;
  apiUrl: string;
  // Add other environment variables as needed
}

export const environment: Environment = {
  production: false,
  apiUrl: 'http://localhost:3000/api'
};
