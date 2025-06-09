import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { PantryService } from '../services/pantry.service';

interface Ingredient {
  id: number;
  name: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatListModule,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  allIngredients: Ingredient[] = [];
  selectedIngredients: Ingredient[] = [];
  searchTerm = '';

  @ViewChild('searchBox') searchBox!: ElementRef<HTMLInputElement>;

  constructor(
    private http: HttpClient,
    private pantry: PantryService,
    private router: Router
  ) {}

  ngOnInit() {
    this.http
      .get<Ingredient[]>('assets/ingredients.json')
      .subscribe((list) => (this.allIngredients = list));
  }

  get filteredAvailable() {
    const term = this.searchTerm.trim().toLowerCase();
    return this.allIngredients
      .filter((i) => !this.isSelected(i))
      .filter((i) => {
        const name = i.name.toLowerCase();
        const words = name.split(/\s+/);
        if (name.startsWith(term)) {
          return true;
        }
        return words.some((w) => w.startsWith(term));
      })
      .sort((a, b) => a.name.localeCompare(b.name));
  }

  isSelected(ing: Ingredient) {
    return this.selectedIngredients.some((x) => x.id === ing.id);
  }

  add(ing: Ingredient) {
    if (!this.isSelected(ing)) {
      this.selectedIngredients = [...this.selectedIngredients, ing];
    }
    this.searchTerm = '';
    this.searchBox?.nativeElement.focus();
  }

  remove(ing: Ingredient) {
    this.selectedIngredients = this.selectedIngredients.filter(
      (x) => x.id !== ing.id
    );
  }

  gotoRecipes() {
    this.pantry.setSelected(this.selectedIngredients.map((i) => i.name));
    this.router.navigate(['/recipes']);
  }
}
