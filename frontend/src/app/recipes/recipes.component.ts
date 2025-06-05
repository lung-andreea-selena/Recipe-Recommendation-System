import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { PantryService } from '../services/pantry.service';
import { RecipeDTO } from '../models/recipe_dto';
import { Subscription } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';
import { LottieComponent } from 'ngx-lottie';
import { AnimationOptions } from 'ngx-lottie';
import { Router } from '@angular/router';

@Component({
  selector: 'app-recipes',
  standalone: true,
  imports: [CommonModule, MatCardModule, LottieComponent],
  templateUrl: './recipes.component.html',
  styleUrls: ['./recipes.component.scss'],
})
export class RecipesComponent implements OnInit, OnDestroy {
  recipes: RecipeDTO[] = [];
  hasMore = false;
  loading = false;

  readonly perPage = 20;

  lottieOptions: AnimationOptions = {
    path: 'assets/loader.json',
    renderer: 'svg',
    autoplay: true,
    loop: true,
  };

  private sub!: Subscription;

  constructor(private pantry: PantryService, private router: Router) {}

  currentPage = 0;

  ngOnInit() {
    this.sub = this.pantry.reload$
      .pipe(
        switchMap((state) => {
          this.loading = true;
          return this.pantry.recommend(state, this.perPage);
        })
      )
      .subscribe((resp) => {
        this.recipes = resp.recipes; // already string[]
        this.hasMore = resp.has_more;
        this.currentPage = resp.page;
        this.loading = false;
      });
  }

  ngOnDestroy() {
    this.sub?.unsubscribe();
  }

  nextPage() {
    this.pantry.setPage(+1);
  }
  prevPage() {
    this.pantry.setPage(-1);
  }
  seeDetails(r: RecipeDTO) {
    this.router.navigate(['/recipes', r.recipe_id]);
  }
}
