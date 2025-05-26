import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { PantryService } from '../services/pantry.service';
import { RecipeDTO } from '../models/recipe_dto';

@Component({
  selector: 'app-recipes',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  templateUrl: './recipes.component.html',
  styleUrls: ['./recipes.component.scss'],
})
export class RecipesComponent implements OnInit {
  recipes: RecipeDTO[] = [];

  constructor(private pantry: PantryService) {}

  ngOnInit() {
    this.pantry.recommend().subscribe((res) => {
      this.recipes = res.recipes;
    });
  }
}
