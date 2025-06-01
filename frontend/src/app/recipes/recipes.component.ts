import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { PantryService } from '../services/pantry.service';
import { RecipeDTO } from '../models/recipe_dto';
import { NavigationEnd, Router } from '@angular/router';
import { filter, Subscription } from 'rxjs';
import { LottieComponent } from 'ngx-lottie';
import { AnimationOptions } from 'ngx-lottie';

@Component({
  selector: 'app-recipes',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    LottieComponent, 
  ],
  templateUrl: './recipes.component.html',
  styleUrls: ['./recipes.component.scss'],
})
export class RecipesComponent implements OnInit, OnDestroy {
  recipes: RecipeDTO[] = [];
  page = 0;
  perPage = 20;

  lottieOptions: AnimationOptions = {
    path: 'assets/loader.json',
    renderer: 'svg',
    autoplay: true,
    loop: true,
  };

  loading = false; 
  private navSub!: Subscription;

  constructor(private pantry: PantryService, private router: Router) {}

  ngOnInit() {
    this.fetchRecipes();

    this.navSub = this.router.events
      .pipe(
        filter((ev) => ev instanceof NavigationEnd),
        filter((ev: NavigationEnd) =>
          ev.urlAfterRedirects.startsWith('/recipes')
        )
      )
      .subscribe(() => {
        this.fetchRecipes();
      });
  }

  ngOnDestroy() {
    this.navSub?.unsubscribe();
  }

  private fetchRecipes() {
    this.loading = true;

    setTimeout(() => {
      this.pantry.recommend(this.page, this.perPage).subscribe(
        (resp) => {
          this.recipes = resp.recipes;
          this.loading = false;
        },
        () => {
          this.loading = false;
        }
      );
    }, 0);
  }

  seeDetails(r: RecipeDTO) {
    this.router.navigate(['/recipes', r.recipe_id]);
  }
}
