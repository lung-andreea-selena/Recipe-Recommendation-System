import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { tap, delay, map } from 'rxjs/operators';
import { RecipeDTO } from '../models/recipe_dto';
import { Recipe } from '../models/recipe_model';

interface RecommendResponse {
  page: number;
  per_page: number;
  has_more: boolean;
  recipes: RecipeDTO[];
}

interface State {
  tokens: string[];
  page: number;
}

@Injectable({ providedIn: 'root' })
export class PantryService {
  private _state: State = { tokens: [], page: 0 };

  private _reload$ = new BehaviorSubject<State>(this._state);
  readonly reload$ = this._reload$.asObservable();

  private cache: {
    key: string;
    data: RecommendResponse;
  } | null = null;

  constructor(private http: HttpClient) {}

  setSelected(tokens: string[]) {
    const normalized = [...tokens].sort();

    // if nothing changed, bail out early
    if (
      normalized.length === this._state.tokens.length &&
      normalized.every((t, i) => t === this._state.tokens[i])
    ) {
      return;
    }

    this._state = { tokens: normalized, page: 0 }; // ⬅ reset page
    this.cache = null;
    this._reload$.next(this._state);
  }

  setPage(delta: number) {
    const newPage = Math.max(0, this._state.page + delta);
    if (newPage === this._state.page) {
      return;
    }

    this._state = { ...this._state, page: newPage };
    this._reload$.next(this._state);
  }

  recommend(state: State, perPage = 20): Observable<RecommendResponse> {
    const key = JSON.stringify({
      tokens: state.tokens,
      page: state.page,
      perPage,
    });

    if (this.cache && this.cache.key === key) {
      return of(this.cache.data).pipe(delay(0));
    }

    return this.http
      .post<RecommendResponse>('/api/recommend', {
        ingredients: state.tokens,
        page: state.page,
        per_page: perPage,
      })
      .pipe(tap((resp) => (this.cache = { key, data: resp })));
  }

  getRecipeById(id: number): Observable<Recipe> {
    return this.http.get<Recipe>(`/api/recipe/${id}`).pipe(
      map((r: any) => ({
        recipe_id: r.recipe_id,
        title: r.title,
        link:
          r.link && !/^https?:\/\//i.test(r.link)
            ? `https://${r.link}`
            : r.link,
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
