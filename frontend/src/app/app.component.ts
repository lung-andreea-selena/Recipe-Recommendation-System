import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { filter } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HeaderComponent, RouterOutlet],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  private isBrowser: boolean;

  constructor(private router: Router, @Inject(PLATFORM_ID) platformId: object) {
    this.isBrowser = isPlatformBrowser(platformId);

    if (this.isBrowser) {
      this.router.events
        .pipe(filter((e) => e instanceof NavigationEnd))
        .subscribe((e: NavigationEnd) => {
          const body = document.body;

          if (e.urlAfterRedirects.startsWith('/recipes')) {
            body.classList.add('recipes-bg');
          } else {
            body.classList.remove('recipes-bg');
          }
        });
    }
  }
}
