export interface RecipeDTO {
  recipe_id: number;
  title: string;
  ingredients: string[];
  has_missing_ingredients: boolean;
}
