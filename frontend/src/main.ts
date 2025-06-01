import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideLottieOptions } from 'ngx-lottie';
import { AppComponent } from './app/app.component';
import { routes } from './app/app.routes';
import { RouteReuseStrategy } from '@angular/router';
import { CacheRouteReuseStrategy } from './app/app-router-reuse-strategy';

export function playerFactory() {
  return import('lottie-web');
}

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(withFetch()),
    {
      provide: RouteReuseStrategy,
      useClass: CacheRouteReuseStrategy,
    },

    provideLottieOptions({
      player: playerFactory,
    }),
  ],
}).catch((err) => console.error(err));
