import { Component, OnInit } from '@angular/core';
import { PantryService, Recipe } from '../services/pantry.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-recipes',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule],
  templateUrl: './recipes.component.html',
  styleUrls: ['./recipes.component.scss'],
})
export class RecipesComponent implements OnInit {
  recipes: Recipe[] = [];

  constructor(private pantry: PantryService, private router: Router) {}

  ngOnInit() {
    this.pantry.recommend().subscribe((res) => {
      this.recipes = res.recipes;
    });
  }

  seeDetails(r: Recipe) {
    this.router.navigate(['/recipes', r.recipe_id]);
  }
}
