// src/app/recipe-details/recipe-details.component.ts

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common'; // ← import Location
import { PantryService } from '../services/pantry.service';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { Recipe } from '../models/recipe_model';

@Component({
  selector: 'app-recipe-details',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule],
  templateUrl: './recipe-details.component.html',
  styleUrls: ['./recipe-details.component.scss'],
})
export class RecipeDetailsComponent implements OnInit {
  recipe: Recipe | null = null;
  loading = true;
  error: string | null = null;

  // Inject ActivatedRoute to get the :id, and Location to goBack()
  constructor(
    private route: ActivatedRoute,
    private pantryService: PantryService,
    private location: Location // ← inject Location instead of Router
  ) {}

  ngOnInit() {
    const idParam = this.route.snapshot.paramMap.get('id');
    const id = idParam ? parseInt(idParam, 10) : null;
    if (id === null) {
      this.error = 'No recipe ID provided';
      this.loading = false;
      return;
    }

    this.pantryService.getRecipeById(id).subscribe(
      (rec) => {
        this.recipe = rec;
        this.loading = false;
      },
      (err) => {
        this.error = 'Recipe not found or error loading';
        this.loading = false;
      }
    );
  }

  goBack() {
    // Instead of re‐navigating to "/recipes" (which triggers a new POST),
    // this simply goes back in the browser history stack to the previously‐rendered list view.
    this.location.back();
  }
}
