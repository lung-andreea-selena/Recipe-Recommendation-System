// src/app/recipe-details/recipe-details.component.ts

import {
  ChangeDetectionStrategy,
  Component,
  Inject,
  OnInit,
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common'; // ← import Location
import { PantryService } from '../services/pantry.service';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { Recipe } from '../models/recipe_model';
import {
  MAT_DIALOG_DATA,
  MatDialogModule,
  MatDialogRef,
} from '@angular/material/dialog';
import { Observable } from 'rxjs';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-recipe-details',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatDialogModule,
    MatListModule,
  ],
  templateUrl: './recipe-details.component.html',
  styleUrls: ['./recipe-details.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RecipeDetailsComponent {
  readonly recipe$: Observable<Recipe>;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { id: number },
    private pantry: PantryService,
    private dialogRef: MatDialogRef<RecipeDetailsComponent>
  ) {
    this.recipe$ = this.pantry.getRecipeById(data.id);
  }

  close(): void {
    this.dialogRef.close();
  }
}
