import { environment } from '../environments/environment';

export class EnvironmentService {
  private static currentEnvironment = environment;

  static setApiUrl(url: string): void {
    this.currentEnvironment.apiUrl = url;
  }

  static setProduction(isProd: boolean): void {
    this.currentEnvironment.production = isProd;
  }

  static getCurrentEnvironment() {
    return this.currentEnvironment;
  }
}
  }
}
