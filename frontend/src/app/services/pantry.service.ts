// src/app/services/pantry.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { tap, delay, map } from 'rxjs/operators';
import { RecipeDTO } from '../models/recipe_dto';
import { Recipe } from '../models/recipe_model';

interface RecommendResponse {
  page: number;
  per_page: number;
  recipes: RecipeDTO[];
}

@Injectable({ providedIn: 'root' })
export class PantryService {
  private selected: string[] = [];
  private cache: {
    key: string;
    data: RecommendResponse;
  } | null = null;

  constructor(private http: HttpClient) {}
  setSelected(ings: string[]) {
    this.selected = [...ings].sort();
    this.cache = null;
  }

  recommend(
    page: number = 0,
    perPage: number = 20
  ): Observable<RecommendResponse> {
    const key = JSON.stringify({
      tokens: this.selected,
      page,
      perPage,
    });

    if (this.cache && this.cache.key === key) {
      return of(this.cache.data).pipe(delay(0));
    }

    return this.http
      .post<RecommendResponse>('/api/recommend', {
        ingredients: this.selected,
        page,
        per_page: perPage,
      })
      .pipe(
        tap((resp) => {
          this.cache = {
            key,
            data: resp,
          };
        })
      );
  }

  getRecipeById(id: number): Observable<Recipe> {
    return this.http.get<Recipe>(`/api/recipe/${id}`).pipe(
      map((r: any) => ({
        recipe_id: r.recipe_id,
        title: r.title,
        link: r.link,
        source: r.source,
        ingredients: Array.isArray(r.ingredients)
          ? r.ingredients
          : typeof r.ingredients === 'string'
          ? JSON.parse(r.ingredients)
          : [],
        directions: Array.isArray(r.directions)
          ? r.directions
          : typeof r.directions === 'string'
          ? JSON.parse(r.directions)
          : [],
      }))
    );
  }
}
