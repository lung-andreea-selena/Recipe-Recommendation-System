import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  OnInit,
  ChangeDetectorRef,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { PantryService } from '../services/pantry.service';
import { RecipeDTO } from '../models/recipe_dto';
import { switchMap } from 'rxjs/operators';
import { LottieComponent } from 'ngx-lottie';
import { AnimationOptions } from 'ngx-lottie';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { RecipeDetailsComponent } from '../recipe-details/recipe-details.component';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Location } from '@angular/common';

@Component({
  selector: 'app-recipes',
  standalone: true,
  imports: [CommonModule, MatCardModule, LottieComponent, MatDialogModule],
  templateUrl: './recipes.component.html',
  styleUrls: ['./recipes.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RecipesComponent implements OnInit {
  recipes: RecipeDTO[] = [];
  hasMore = false;
  loading = false;
  currentPage = 0;
  readonly perPage = 20;

  lottieOptions: AnimationOptions = {
    path: 'assets/loader.json',
    renderer: 'svg',
    autoplay: true,
    loop: true,
  };

  constructor(
    private pantry: PantryService,
    private dialog: MatDialog,
    private destroyRef: DestroyRef,
    private cdr: ChangeDetectorRef,
    private location: Location
  ) {}

  ngOnInit() {
    this.pantry.reload$
      .pipe(
        switchMap((state) => {
          this.loading = true;
          this.cdr.markForCheck();
          return this.pantry.recommend(state, this.perPage);
        }),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe((resp) => {
        this.recipes = resp.recipes;
        this.hasMore = resp.has_more;
        this.currentPage = resp.page;
        this.loading = false;
        this.cdr.markForCheck();
      });
  }

  nextPage() {
    this.pantry.setPage(+1);
  }
  prevPage() {
    this.pantry.setPage(-1);
  }
  openDialog(id: number): void {
    this.location.go(`/recipes/${id}`);

    const ref = this.dialog.open(RecipeDetailsComponent, {
      maxWidth: '600px',
      width: '95%',
      data: { id },
      panelClass: 'details-dialog',
    });

    ref.afterClosed().subscribe(() => {
      this.location.go('/recipes');
    });
  }
}
