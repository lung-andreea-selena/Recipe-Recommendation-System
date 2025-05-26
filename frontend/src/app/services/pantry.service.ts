// src/app/services/pantry.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { RecipeDTO } from '../models/recipe_dto';

interface RecommendResponse {
  page: number;
  per_page: number;
  recipes: RecipeDTO[];
}

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
  ): Observable<RecommendResponse> {
    return this.http.post<RecommendResponse>('/api/recommend', {
      ingredients: this.selected,
      page,
      per_page: perPage,
    });
  }
}
