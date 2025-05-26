import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';

export interface Recipe {
  recipe_id: number;
  title: string;
  ingredients: string[];
  directions: string[];
  link: string;
  source: string;
}

const BACKEND = 'http://localhost:5000';

@Injectable({ providedIn: 'root' })
export class PantryService {
  private selected: string[] = [];

  constructor(private http: HttpClient) {}

  setSelected(ings: string[]) {
    this.selected = ings;
  }

  recommend(
    page: number = 0,
    perPage: number = 20
  ): Observable<{ page: number; per_page: number; recipes: Recipe[] }> {
    return this.http
      .post<{ page: number; per_page: number; recipes: any[] }>(
        '/api/recommend',
        { ingredients: this.selected, page, per_page: perPage }
      )
      .pipe(
        map((resp: { recipes: any[]; page: any; per_page: any }) => {
          const recipes: Recipe[] = resp.recipes.map((r: any) => ({
            recipe_id: r.recipe_id,
            title: r.title,
            link: r.link,
            source: r.source,
            ingredients: Array.isArray(r.ingredients)
              ? r.ingredients
              : JSON.parse(r.ingredients),
            directions: Array.isArray(r.directions)
              ? r.directions
              : JSON.parse(r.directions),
          }));

          return {
            page: resp.page,
            per_page: resp.per_page,
            recipes,
          };
        })
      );
  }
}
